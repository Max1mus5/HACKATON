
// Configuración del chatbot
const config = {
    threshold: 0.28,
    mode: "adaptativo",
    debugMode: false,
    useExternalLLM: true,  // Habilitar el uso de LLM externo
    geminiAPIKey: typeof API_CONFIG !== 'undefined' ? API_CONFIG.geminiApiKey : "",  // Cargar desde config.js
    geminiModel: "gemini-1.5-flash-latest",  // Modelo de Gemini a utilizar
    apiTested: false, // Indicador de si la API ha sido probada
    apiWorking: false // Indicador de si la API está funcionando
};

// Función para cargar y mostrar el historial de mensajes
async function loadChatHistory() {
    if (window.leanBotAPI && window.leanBotAPI.isBackendAvailable) {
        try {
            console.log('📋 Cargando historial de chat...');
            const chatHistory = await window.leanBotAPI.getChatHistory();
            
            const chatWindow = document.getElementById("messages-container");
            if (chatHistory && chatHistory.length > 0) {
                // Limpiar chat window antes de cargar historial
                chatWindow.innerHTML = '';
                
                // Mostrar cada mensaje del historial con la estructura correcta
                chatHistory.forEach(messageData => {
                    // Verificar que el mensaje tiene la estructura correcta
                    if (messageData.message && messageData.response) {
                        // Mensaje del usuario con estilos correctos
                        const userMessage = document.createElement("div");
                        userMessage.classList.add("message", "user-message");
                        userMessage.innerHTML = `
                            <div class="message-avatar user-avatar">
                                <span>U</span>
                            </div>
                            <div class="message-content">
                                <div class="message-text">${messageData.message}</div>
                                <div class="message-time">${new Date(messageData.timestamp).toLocaleTimeString()}</div>
                            </div>
                        `;
                        chatWindow.appendChild(userMessage);
                        
                        // Respuesta del bot con estilos correctos
                        const botMessage = document.createElement("div");
                        botMessage.classList.add("message", "bot-message");
                        botMessage.innerHTML = `
                            <div class="message-avatar bot-avatar">
                                <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                            </div>
                            <div class="message-content">
                                <div class="message-text">${messageData.response}</div>
                                <div class="message-time">${new Date(messageData.timestamp).toLocaleTimeString()}</div>
                            </div>
                        `;
                        chatWindow.appendChild(botMessage);
                        
                        // Log del score y timestamp para debugging (opcional)
                        if (config.debugMode) {
                            console.log(`Mensaje cargado - Score: ${messageData.score}, Timestamp: ${messageData.timestamp}`);
                        }
                    }
                });
                
                // Desplazarse al final del chat
                chatWindow.scrollTop = chatWindow.scrollHeight;
                console.log(`✅ Historial cargado: ${chatHistory.length} conversaciones`);
            } else {
                console.log('📋 No hay historial previo');
            }
        } catch (error) {
            console.error('❌ Error al cargar historial:', error);
        }
    }
}

// Cargar la clave API desde localStorage si existe
document.addEventListener("DOMContentLoaded", function() {
    // Cargar clave desde localStorage si está disponible (esto tiene prioridad)
    const savedApiKey = localStorage.getItem('gemini_api_key');
    const savedModel = localStorage.getItem('gemini_model');
    
    if (savedApiKey) {
        config.geminiAPIKey = savedApiKey;
        console.log("✅ Clave API cargada desde localStorage");
        
        // Actualizar también en otros lugares si existen
        if (window.ENV_CONFIG && window.ENV_CONFIG.geminiAPIKey !== undefined) {
            window.ENV_CONFIG.geminiAPIKey = savedApiKey;
        }
        if (window.API_CONFIG && window.API_CONFIG.geminiApiKey !== undefined) {
            window.API_CONFIG.geminiApiKey = savedApiKey;
        }
    }
    
    if (savedModel) {
        config.geminiModel = savedModel;
        console.log("✅ Modelo Gemini cargado desde localStorage:", savedModel);
    }
    
    // Resetear estados de API para forzar nueva verificación
    config.apiTested = false;
    config.apiWorking = false;
    
    // Cargar historial después de que LEAN BOT se inicialice
    setTimeout(async () => {
        await loadChatHistory();
    }, 2000); // Aumentado a 2 segundos para asegurar que LEAN BOT se inicialice correctamente
});

// Cargar corpus de datos
let corpus = null;
let questions = [];
let answers = [];

// Función para cargar el corpus desde data.json
async function loadCorpus() {
    try {
        // Cargar datos desde la estructura pública
        const response = await fetch('./data/data.json');
        corpus = await response.json();
        
        // Preparar las preguntas y respuestas para vectorización
        corpus.faq.forEach(item => {
            questions.push(item.question.toLowerCase());
            answers.push(item.answer);
        });
        
        console.log('Corpus cargado con éxito:', corpus.faq.length, 'pares de preguntas/respuestas');
        return true;
    } catch (error) {
        console.error('Error al cargar el corpus:', error);
        // Mostrar más detalles sobre el error para facilitar la depuración
        console.error('Detalles del error:', error.message);
        return false;
    }
}

// Sinónimos y términos relacionados (basado en el diccionario del notebook)
const terminos_ampliados = {
    // Términos relacionados con el proyecto
    "título": ["nombre", "denominación", "tema", "proyecto"],
    "proyecto": ["estudio", "investigación", "trabajo", "iniciativa"],
    "exposición": ["radiación", "emisión", "campos"],
    "electromagnética": ["electromagnetismo", "electromagnético", "radiación", "EMF"],
    "machine learning": ["ml", "aprendizaje automático", "aprendizaje de máquina", "ia", "inteligencia artificial"],
    
    // Términos relacionados con objetivos
    "objetivos": ["metas", "propósitos", "fines", "finalidad"],
    "general": ["principal", "primario", "central"],
    "específicos": ["secundarios", "concretos", "particulares"],
    
    // Términos relacionados con modelos
    "modelos": ["algoritmos", "técnicas", "métodos", "enfoques"],
    "regresión": ["predicción", "estimación"],
    "árboles": ["decision trees", "árbol de decisión"],
    "random forest": ["bosque aleatorio", "rf"],
    "xgboost": ["gradient boosting", "boosting"],
    
    // Términos relacionados con datos
    "datos": ["información", "dataset", "conjunto de datos", "fuentes"],
    "variables": ["características", "features", "atributos", "parámetros"],
    
    // Términos relacionados con el problema
    "problema": ["desafío", "reto", "cuestión", "dificultad"],
    "planteamiento": ["formulación", "definición", "descripción"],
    
    // Términos relacionados con beneficios
    "beneficios": ["ventajas", "utilidad", "provecho", "aportes"],
    "ventajas": ["beneficios", "fortalezas", "puntos fuertes"],
    
    // Términos relacionados con conclusiones
    "conclusiones": ["resultados", "hallazgos", "descubrimientos", "inferencias"],
    
    // Añadir términos específicos para participantes
    "participantes": ["integrantes", "miembros", "colaboradores", "personas", "equipo", "autores", "investigadores"],
    "equipo": ["grupo", "personal", "staff", "integrantes", "miembros", "participantes"],
    "andres": ["mauricio", "ardila", "andres mauricio", "andres ardila", "mauricio ardila"],
    "claudia": ["ines", "giraldo", "claudia ines", "claudia giraldo", "ines giraldo"],
    "marisela": ["lotero", "zuluaga", "marisela lotero", "marisela zuluaga", "lotero zuluaga"],
    "darly": ["mildred", "delgado", "darly mildred", "darly delgado", "mildred delgado"]
};

// Función para expandir términos, similar a la del notebook
function expandirTerminos(texto) {
    // Convertir a minúsculas para comparación
    let textoLower = texto.toLowerCase();
    let textoExpandido = textoLower;
    
    // Buscar términos clave en el texto
    Object.keys(terminos_ampliados).forEach(termino => {
        if (textoLower.includes(termino)) {
            // Añadir términos relacionados al texto expandido
            const terminosAdicionales = terminos_ampliados[termino].join(' ');
            textoExpandido += ' ' + terminosAdicionales;
        }
    });
    
    return textoExpandido;
}

// Preprocesamiento de texto mejorado con expansión de términos
function preprocessText(text) {
    // Convertir a minúsculas y eliminar caracteres especiales
    let processed = text.toLowerCase().replace(/[^\w\sáéíóúüñ]/gi, '');
    
    // Expansión de términos
    processed = expandirTerminos(processed);
    
    return processed;
}

// Tokenizar texto (similar a word_tokenize)
function tokenize(text) {
    return text.split(/\s+/).filter(token => token.length > 0);
}

// Calcular similitud coseno entre dos vectores
function cosineSimilarity(vecA, vecB) {
    const dotProduct = Object.keys(vecA).reduce((sum, key) => {
        return sum + (vecA[key] * (vecB[key] || 0));
    }, 0);
    
    const magnitudeA = Math.sqrt(Object.values(vecA).reduce((sum, val) => sum + val * val, 0));
    const magnitudeB = Math.sqrt(Object.values(vecB).reduce((sum, val) => sum + val * val, 0));
    
    return dotProduct / (magnitudeA * magnitudeB) || 0;
}

// Convertir texto a vector TF-IDF simplificado
function textToVector(text, allTexts) {
    const tokens = tokenize(preprocessText(text));
    const vector = {};
    
    tokens.forEach(token => {
        // Contar ocurrencias del token en el texto actual
        vector[token] = (vector[token] || 0) + 1;
    });
    
    // Aplicar TF-IDF simplificado
    Object.keys(vector).forEach(token => {
        // Calcular cuántos documentos contienen este token
        const docsWithToken = allTexts.filter(t => t.includes(token)).length;
        
        // IDF: log(totalDocs / docsWithToken)
        const idf = Math.log(allTexts.length / (docsWithToken || 1));
        
        // TF: frecuencia del término en el documento
        const tf = vector[token];
        
        // TF-IDF
        vector[token] = tf * idf;
    });
    
    return vector;
}

// Modificar función findBestResponse para retornar también la similitud
function findBestResponse(userQuestion) {
    // Procesar la pregunta del usuario
    const processedQuestion = preprocessText(userQuestion);
    
    // Crear una lista con todas las preguntas del corpus más la del usuario
    const allTexts = [...questions, processedQuestion];
    
    // Vectorizar todas las preguntas
    const vectors = allTexts.map(text => textToVector(text, allTexts));
    
    // Calcular similitudes entre la pregunta del usuario y todas las preguntas del corpus
    const similarities = [];
    for (let i = 0; i < questions.length; i++) {
        similarities.push(cosineSimilarity(vectors[vectors.length-1], vectors[i]));
    }
    
    // Encontrar el índice de la pregunta más similar
    const maxIndex = similarities.indexOf(Math.max(...similarities));
    const maxSimilarity = similarities[maxIndex];
    
    // Aplicar umbral según configuración
    if (config.debugMode) {
        console.log(`Pregunta más similar: "${questions[maxIndex]}" con similitud: ${maxSimilarity}`);
    }
    
    if (maxSimilarity < config.threshold) {
        return {
            response: "Lo siento, no tengo una respuesta para esa pregunta. Por favor, intenta con otra consulta.",
            similarity: maxSimilarity
        };
    }
    
    // Devolver la respuesta correspondiente y su similitud
    return {
        response: answers[maxIndex],
        similarity: maxSimilarity
    };
}

// Función para probar la conexión con la API de Gemini
async function testGeminiAPI() {
    try {
        // Si ya se ha probado la API, no es necesario hacerlo de nuevo
        if (config.apiTested) {
            return config.apiWorking;
        }
        
        // Verificar si hay una clave API configurada
        if (!config.geminiAPIKey || config.geminiAPIKey === "") {
            console.warn("API Key para Gemini no configurada");
            config.apiTested = true;
            config.apiWorking = false;
            return false;
        }
        
        console.log("Probando conexión con la API de Gemini...");
        
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${config.geminiModel}:generateContent?key=${config.geminiAPIKey}`;
        
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                contents: [
                    {
                        role: "user",
                        parts: [
                            {
                                text: "Responde únicamente con la palabra 'OK' para verificar que la conexión está funcionando."
                            }
                        ]
                    }
                ],
                generationConfig: {
                    temperature: 0.1,
                    maxOutputTokens: 10,
                    topP: 0.95
                }
            })
        });
        
        const data = await response.json();
        
        // Verificar que la respuesta sea válida
        if (data.candidates && data.candidates.length > 0 && 
            data.candidates[0].content && 
            data.candidates[0].content.parts && 
            data.candidates[0].content.parts.length > 0) {
            config.apiTested = true;
            config.apiWorking = true;
            console.log("Conexión con la API de Gemini establecida correctamente");
            return true;
        } else {
            console.error("Prueba de API de Gemini falló:", data);
            config.apiTested = true;
            config.apiWorking = false;
            return false;
        }
    } catch (error) {
        console.error("Error al probar la API de Gemini:", error);
        config.apiTested = true;
        config.apiWorking = false;
        return false;
    }
}

// Función para consultar a Gemini API
async function askExternalLLM(question) {
    try {
        // Verificar si la API está funcionando antes de intentar usarla
        if (!await testGeminiAPI()) {
            console.warn("No se puede usar la API de Gemini, no está configurada correctamente");
            return null;
        }
        
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${config.geminiModel}:generateContent?key=${config.geminiAPIKey}`;
        
        // Establecer un timeout para la petición
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 segundos de timeout
        
        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    contents: [
                        {
                            role: "user",
                            parts: [
                                {
                                    text: "Eres un asistente virtual que proporciona respuestas breves y concisas a preguntas generales. Limita tus respuestas a 2-3 oraciones. Aquí está mi pregunta: " + question
                                }
                            ]
                        }
                    ],
                    generationConfig: {
                        temperature: 0.7,
                        maxOutputTokens: 150,
                        topP: 0.95
                    }
                }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId); // Limpiar el timeout si la petición se completa
            
            const data = await response.json();
            
            // Manejar la respuesta de Gemini
            if (data.candidates && data.candidates.length > 0 && 
                data.candidates[0].content && 
                data.candidates[0].content.parts && 
                data.candidates[0].content.parts.length > 0) {
                return data.candidates[0].content.parts[0].text.trim();
            } else {
                console.error("No se recibió una respuesta válida de la API de Gemini:", data);
                return null;
            }
        } catch (fetchError) {
            clearTimeout(timeoutId);
            if (fetchError.name === 'AbortError') {
                console.error("La petición a la API de Gemini excedió el tiempo límite");
                return null;
            }
            throw fetchError;
        }
    } catch (error) {
        console.error("Error al consultar la API de Gemini:", error);
        return null;
    }
}

// Función para saludos
function greetingResponse(text) {
    const greetings = ["hola", "buenas", "saludos", "qué tal", "hey", "buenos días", "buenas tardes", "buenas noches"];
    const greetingReplies = [
        "¡Hola! Soy LEAN BOT, el asistente virtual de INGE LEAN. ¿Cómo puedo ayudarte?",
        "¡Hola! Soy LEAN BOT de INGE LEAN. ¿En qué puedo asistirte?",
        "¡Saludos! Soy LEAN BOT, tu asistente virtual de INGE LEAN. Dime, ¿cómo puedo ayudarte?"
    ];
    
    for (const word of text.split(' ')) {
        if (greetings.includes(word.toLowerCase())) {
            return greetingReplies[Math.floor(Math.random() * greetingReplies.length)];
        }
    }
    
    return null;
}

// Función para despedidas
function farewellResponse() {
    const farewells = [
        "¡Hasta pronto! Fue un placer ayudarte. Soy LEAN BOT de INGE LEAN, ¡cuídate!",
        "¡Nos vemos! Espero haberte ayudado. LEAN BOT siempre a tu servicio.",
        "¡Chao! Que tengas un excelente día. LEAN BOT de INGE LEAN estará aquí cuando me necesites."
    ];
    
    return farewells[Math.floor(Math.random() * farewells.length)];
}

// Función principal que maneja las respuestas del chatbot
async function getBotResponse(userInput) {
    // IMPORTANTE: Si LEAN BOT backend está disponible, no usar esta función
    // para evitar duplicaciones. Esta función es solo para fallback local.
    if (window.leanBotAPI && window.leanBotAPI.isBackendAvailable) {
        console.log('⚠️ Backend disponible, no usar getBotResponse local para evitar duplicación');
        return "Error: No usar función local cuando backend está disponible";
    }

    // Fallback al sistema local original solo si LEAN BOT no está disponible
    console.log('🔄 Usando sistema de respuestas local como fallback...');
    
    // Asegurarse de que el corpus esté cargado
    if (!corpus) {
        const loaded = await loadCorpus();
        if (!loaded) {
            return "Soy LEAN BOT de INGE LEAN. No puedo responder en este momento debido a problemas técnicos.";
        }
    }
    
    // Corrección ortográfica básica (simplificada de corregir_entrada)
    const userText = userInput.toLowerCase().trim();
    
    // Verificar si es despedida
    if (['salir', 'adiós', 'adios', 'hasta luego', 'bye', 'chao'].includes(userText)) {
        return farewellResponse();
    }
    
    // Verificar si es agradecimiento
    if (['gracias', 'muchas gracias', 'te lo agradezco'].includes(userText)) {
        return "De nada, para eso estoy aquí. Soy LEAN BOT, el asistente de INGE LEAN.";
    }
    
    // Verificar si es ayuda
    if (userText === 'ayuda') {
        return "Hola, soy LEAN BOT, el asistente virtual de INGE LEAN. Puedes preguntarme sobre los participantes, objetivos, conclusiones, modelos, etc. También puedo responder preguntas generales. Si quieres salir, escribe 'salir'.";
    }
    
    // Verificar si es un saludo
    const greetingReply = greetingResponse(userText);
    if (greetingReply) {
        return `${greetingReply} Soy LEAN BOT, tu asistente virtual de INGE LEAN.`;
    }
    
    // Detectar si la pregunta parece ser sobre el proyecto
    const projectKeywords = ["proyecto", "exposición", "electromagnética", "objetivos", "modelos", 
                            "machine learning", "participantes", "ardila", "claudia", "marisela", 
                            "darly", "conclusiones", "mintic", "bootcamp"];
    
    const isProjectQuestion = projectKeywords.some(keyword => userText.includes(keyword));
    
    // Buscar la mejor respuesta en nuestro corpus
    const bestResponseResult = findBestResponse(userText);
    const { response, similarity } = bestResponseResult;
    
    // Si la similitud es alta o la pregunta parece ser sobre el proyecto, usar la respuesta del corpus
    if (similarity >= config.threshold || isProjectQuestion) {
        return response;
    }
    
    // Verificar si la API está configurada y activa antes de intentar usarla
    let apiConfigured = Boolean(config.geminiAPIKey && config.geminiAPIKey.trim() !== "");
    
    // Solo si la pregunta no parece ser sobre el proyecto, la similitud es baja, y la API está configurada, intentar usarla
    if (config.useExternalLLM && apiConfigured) {
        try {
            console.log("Consultando a Gemini para respuesta externa...");
            const llmResponse = await askExternalLLM(userInput);
            if (llmResponse) {
                return `${llmResponse}\n\n(Respuesta de LEAN BOT usando Gemini)`;
            }
        } catch (error) {
            console.error("Error al usar el LLM externo:", error);
            // Si hay un error con la API, continuar y usar la respuesta del corpus
        }
    }
    
    // Si no hay respuesta del LLM, la API no está configurada, o está desactivada, devolver la respuesta del corpus
    return response;
}

// Función para ocultar parcialmente un texto, mostrando solo algunos caracteres
function partiallyMaskText(text, visibleStart = 4, visibleEnd = 4) {
    if (!text || text.length < 8) return text; // Si es muy corta, no aplicar máscara
    
    const start = text.substring(0, visibleStart);
    const middle = text.substring(visibleStart, text.length - visibleEnd).replace(/./g, '*');
    const end = text.substring(text.length - visibleEnd);
    
    return start + middle + end;
}

document.addEventListener("DOMContentLoaded", function() {
    const userInputField = document.getElementById("chat-input"); // Corregido de "user-input" a "chat-input"
    const chatButton = document.getElementById("send-btn"); // Corregido de "chat-button" a "send-btn"
    const chatWindow = document.getElementById("messages-container"); // Corregido para usar el contenedor correcto
    const micButton = document.getElementById("mic-button");
    
    // Elementos para el modal de configuración
    const settingsButton = document.getElementById("settings-nav"); // Corregido para usar el nav de configuración
    const settingsModal = document.getElementById("settings-modal");
    const closeModalButton = document.querySelector(".close");
    const apiKeyInput = document.getElementById("api-key-input");
    const geminiModelSelect = document.getElementById("gemini-model-select");
    const saveApiSettings = document.getElementById("save-api-settings");
    const testApiConnection = document.getElementById("test-api-connection");
    const apiTestResult = document.getElementById("api-test-result");
    const togglePasswordButton = document.getElementById("toggle-password");
    
    // Variables para controlar el estado de visualización de la clave API
    let apiKeyFullyVisible = false;
    let originalApiKeyValue = '';
    
    // Funcionalidad para mostrar/ocultar la clave API
    if (togglePasswordButton) {
        togglePasswordButton.addEventListener("click", function() {
            if (apiKeyInput.type === "password") {
                // Guardar el valor original antes de mostrarlo parcialmente
                originalApiKeyValue = apiKeyInput.value;
                
                // Cambiar a tipo texto y mostrar parcialmente la clave
                apiKeyInput.type = "text";
                if (!apiKeyFullyVisible) {
                    apiKeyInput.value = partiallyMaskText(originalApiKeyValue, 5, 5);
                }
                
                togglePasswordButton.innerHTML = '<i class="fas fa-eye-slash"></i>';
                togglePasswordButton.title = apiKeyFullyVisible ? "Mostrar parcialmente" : "Mostrar completamente";
            } else {
                if (!apiKeyFullyVisible) {
                    // Si estaba parcialmente visible, ahora mostrar completamente
                    apiKeyInput.value = originalApiKeyValue;
                    apiKeyFullyVisible = true;
                    togglePasswordButton.title = "Ocultar clave";
                } else {
                    // Si estaba completamente visible, volver a ocultar
                    apiKeyInput.type = "password";
                    apiKeyInput.value = originalApiKeyValue; // Restaurar valor original
                    apiKeyFullyVisible = false;
                    togglePasswordButton.innerHTML = '<i class="fas fa-eye"></i>';
                    togglePasswordButton.title = "Mostrar parcialmente";
                }
            }
        });
        
        // Al enfocar el campo, mostrar siempre el valor completo
        apiKeyInput.addEventListener("focus", function() {
            if (apiKeyInput.type === "text" && !apiKeyFullyVisible) {
                apiKeyInput.value = originalApiKeyValue;
            }
        });
        
        // Al perder el foco, volver a la visualización parcial si está en modo texto
        apiKeyInput.addEventListener("blur", function() {
            if (apiKeyInput.type === "text" && !apiKeyFullyVisible) {
                apiKeyInput.value = partiallyMaskText(originalApiKeyValue, 5, 5);
            }
        });
    }
    
    // Cargar configuración guardada al inicio
    if (localStorage.getItem('gemini_api_key')) {
        const savedKey = localStorage.getItem('gemini_api_key');
        apiKeyInput.value = savedKey;
        originalApiKeyValue = savedKey; // Actualizar también la variable de control
    }
    
    if (localStorage.getItem('gemini_model')) {
        geminiModelSelect.value = localStorage.getItem('gemini_model');
    }
    
    // Abrir modal de configuración
    settingsButton.onclick = function() {
        // Recargar valores más recientes cada vez que se abre el modal
        const currentApiKey = localStorage.getItem('gemini_api_key') || config.geminiAPIKey || '';
        const currentModel = localStorage.getItem('gemini_model') || config.geminiModel || 'gemini-1.5-flash-latest';
        
        apiKeyInput.value = currentApiKey;
        originalApiKeyValue = currentApiKey;
        geminiModelSelect.value = currentModel;
        
        console.log('🔧 Modal abierto con configuración actual:', {
            hasApiKey: currentApiKey ? 'Sí' : 'No',
            model: currentModel
        });
        
        settingsModal.style.display = "block";
    }
    
    // Cerrar modal
    closeModalButton.onclick = function() {
        settingsModal.style.display = "none";
    }
    
    // Cerrar modal al hacer clic fuera de él
    window.onclick = function(event) {
        if (event.target == settingsModal) {
            settingsModal.style.display = "none";
        }
    }
    
    // Guardar configuración de API
    saveApiSettings.onclick = async function() {
        const apiKey = apiKeyInput.value.trim();
        const modelName = geminiModelSelect.value;
        
        console.log('🔧 Iniciando guardado de configuración de API...');
        console.log('📝 API Key presente:', apiKey ? 'Sí' : 'No');
        console.log('📝 Modelo seleccionado:', modelName);
        
        // Limpiar cualquier configuración anterior para evitar conflictos
        config.apiTested = false;
        config.apiWorking = false;
        
        // Actualizar configuración local PRIMERO
        config.geminiAPIKey = apiKey;
        config.geminiModel = modelName;
        
        // Guardar en localStorage (esto sobrescribirá cualquier valor anterior)
        localStorage.setItem('gemini_api_key', apiKey);
        localStorage.setItem('gemini_model', modelName);
        console.log('💾 Configuración actualizada en localStorage');
        
        // Actualizar también en ENV_CONFIG si existe
        if (window.ENV_CONFIG && window.ENV_CONFIG.geminiAPIKey !== undefined) {
            window.ENV_CONFIG.geminiAPIKey = apiKey;
            console.log('🔧 API Key actualizada en ENV_CONFIG');
        }
        
        // Actualizar en API_CONFIG si existe
        if (window.API_CONFIG && window.API_CONFIG.geminiApiKey !== undefined) {
            window.API_CONFIG.geminiApiKey = apiKey;
            console.log('🔧 API Key actualizada en API_CONFIG');
        }
        
        // Enviar API key al backend
        if (apiKey) {
            try {
                // Backend URL hardcodeado apuntando a Render
                const backendURL = 'https://hackaton-d1h6.onrender.com';
                
                console.log('🌐 Enviando API key al backend:', backendURL);
                
                const response = await fetch(`${backendURL}/config/gemini_api_key`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        api_key: apiKey
                    })
                });
                
                console.log('📡 Respuesta del backend - Status:', response.status);
                
                if (response.ok) {
                    const result = await response.json();
                    console.log('✅ API key enviada al backend exitosamente:', result);
                    
                    // Mostrar mensaje de éxito en el modal
                    apiTestResult.innerHTML = `
                        <div style="color: green; font-weight: bold;">
                            ✅ Configuración guardada y enviada al backend correctamente
                        </div>
                        <div style="font-size: 0.9em; margin-top: 5px;">
                            Backend URL: ${backendURL}<br>
                            Respuesta: ${result.message}
                        </div>
                    `;
                    apiTestResult.className = "mt-3 success";
                    
                    // Mostrar mensaje en el chat si existe
                    if (chatWindow) {
                        const botMessage = document.createElement("div");
                        botMessage.classList.add("message", "bot-message");
                        botMessage.innerHTML = `
                            <div class="message-avatar bot-avatar">
                                <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                            </div>
                            <div class="message-content">
                                <div class="message-text">
                                    <strong>🔧 Configuración Actualizada</strong><br>
                                    La API key de Gemini ha sido configurada correctamente tanto en el frontend como en el backend.<br>
                                    <small>✅ LEAN BOT ahora está completamente integrado con Gemini AI</small>
                                </div>
                                <div class="message-time">${new Date().toLocaleTimeString()}</div>
                            </div>
                        `;
                        chatWindow.appendChild(botMessage);
                        chatWindow.scrollTop = chatWindow.scrollHeight;
                    }
                } else {
                    const errorText = await response.text();
                    console.error('❌ Error del backend:', response.status, errorText);
                    throw new Error(`Error ${response.status}: ${errorText}`);
                }
                
            } catch (error) {
                console.warn('⚠️ No se pudo enviar API key al backend:', error);
                
                // Mostrar mensaje de advertencia en el modal
                apiTestResult.innerHTML = `
                    <div style="color: orange; font-weight: bold;">
                        ⚠️ Configuración guardada localmente
                    </div>
                    <div style="font-size: 0.9em; margin-top: 5px;">
                        Error al conectar con backend: ${error.message}<br>
                        La configuración está guardada y funcionará localmente.
                    </div>
                `;
                apiTestResult.className = "mt-3 warning";
                
                // Mostrar mensaje en el chat si existe
                if (chatWindow) {
                    const botMessage = document.createElement("div");
                    botMessage.classList.add("message", "bot-message");
                    botMessage.innerHTML = `
                        <div class="message-avatar bot-avatar">
                            <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                        </div>
                        <div class="message-content">
                            <div class="message-text">
                                <strong>🔧 Configuración Guardada</strong><br>
                                La API key de Gemini ha sido guardada localmente.<br>
                                <small>ℹ️ Se intentará sincronizar con el backend cuando esté disponible</small>
                            </div>
                            <div class="message-time">${new Date().toLocaleTimeString()}</div>
                        </div>
                    `;
                    chatWindow.appendChild(botMessage);
                    chatWindow.scrollTop = chatWindow.scrollHeight;
                }
            }
        } else {
            // Solo guardar localmente si no hay API key
            console.log('ℹ️ No se proporcionó API key, solo guardando configuración local');
            apiTestResult.innerHTML = `
                <div style="color: blue;">
                    ℹ️ Configuración guardada localmente
                </div>
                <div style="font-size: 0.9em; margin-top: 5px;">
                    No se envió API key al backend (campo vacío)
                </div>
            `;
            apiTestResult.className = "mt-3 success";
            
            // Mostrar mensaje en el chat si existe
            if (chatWindow) {
                const botMessage = document.createElement("div");
                botMessage.classList.add("message", "bot-message");
                botMessage.innerHTML = `
                    <div class="message-avatar bot-avatar">
                        <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                    </div>
                    <div class="message-content">
                        <div class="message-text">
                            Configuración actualizada. Para obtener mejores respuestas, considera agregar una API key de Gemini.
                        </div>
                        <div class="message-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                `;
                chatWindow.appendChild(botMessage);
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        }
        
        // Cerrar modal después de un momento
        setTimeout(() => {
            settingsModal.style.display = "none";
        }, 3000); // Aumentado el tiempo para poder leer el mensaje
    }
    
    // Probar conexión con la API
    testApiConnection.onclick = async function() {
        const apiKey = apiKeyInput.value.trim();
        const modelName = geminiModelSelect.value;
        
        console.log('🧪 Iniciando prueba de conexión con API de Gemini...');
        
        if (!apiKey) {
            console.log('❌ No se proporcionó API key para la prueba');
            apiTestResult.innerHTML = `
                <div style="color: red; font-weight: bold;">
                    ❌ Por favor, ingresa una clave API válida
                </div>
            `;
            apiTestResult.className = "mt-3 error";
            return;
        }
        
        // Mostrar cargando
        apiTestResult.innerHTML = `
            <div style="color: blue;">
                🔄 Probando conexión con Gemini API...
            </div>
        `;
        apiTestResult.className = "mt-3";
        
        // Guardar configuración original para restaurar si es necesario
        const originalKey = config.geminiAPIKey;
        const originalModel = config.geminiModel;
        const originalTested = config.apiTested;
        const originalWorking = config.apiWorking;
        
        try {
            console.log('📝 Configurando API temporalmente para prueba...');
            // Actualizar configuración temporalmente con los valores del modal
            config.geminiAPIKey = apiKey;
            config.geminiModel = modelName;
            config.apiTested = false;
            config.apiWorking = false;
            
            // Probar API directamente
            console.log('📡 Enviando prueba a Gemini API...');
            const success = await testGeminiAPI();
            
            if (success) {
                console.log('✅ Prueba de API exitosa');
                apiTestResult.innerHTML = `
                    <div style="color: green; font-weight: bold;">
                        ✅ ¡Conexión exitosa!
                    </div>
                    <div style="font-size: 0.9em; margin-top: 5px;">
                        La API de Gemini está funcionando correctamente<br>
                        Modelo: ${modelName}
                    </div>
                `;
                apiTestResult.className = "mt-3 success";
                
                // También probar el backend si está disponible
                if (window.leanBotAPI && window.leanBotAPI.isBackendAvailable) {
                    try {
                        console.log('🔄 Probando integración con backend...');
                        const backendTest = await window.leanBotAPI.testGeminiConnection();
                        console.log('🧪 Resultado de prueba del backend:', backendTest);
                        
                        if (backendTest.status === 'success') {
                            apiTestResult.innerHTML += `
                                <div style="color: green; margin-top: 10px;">
                                    🤖 Backend también confirmó conexión exitosa
                                </div>
                            `;
                        }
                    } catch (backendError) {
                        console.warn('⚠️ Error al probar backend:', backendError);
                    }
                }
            } else {
                console.log('❌ Prueba de API falló');
                apiTestResult.innerHTML = `
                    <div style="color: red; font-weight: bold;">
                        ❌ No se pudo conectar con la API de Gemini
                    </div>
                    <div style="font-size: 0.9em; margin-top: 5px;">
                        Verifica que tu clave API sea válida y tenga permisos para el modelo ${modelName}
                    </div>
                `;
                apiTestResult.className = "mt-3 error";
                
                // Restaurar configuración original si la prueba falla
                config.geminiAPIKey = originalKey;
                config.geminiModel = originalModel;
                config.apiTested = originalTested;
                config.apiWorking = originalWorking;
            }
        } catch (error) {
            console.error("❌ Error durante la prueba de API:", error);
            apiTestResult.innerHTML = `
                <div style="color: red; font-weight: bold;">
                    ❌ Error al probar la conexión
                </div>
                <div style="font-size: 0.9em; margin-top: 5px;">
                    ${error.message}
                </div>
            `;
            apiTestResult.className = "mt-3 error";
            
            // Restaurar configuración original si hay un error
            config.geminiAPIKey = originalKey;
            config.geminiModel = originalModel;
            config.apiTested = originalTested;
            config.apiWorking = originalWorking;
        }
    }

    // Función para enviar mensaje
    async function sendMessage() {
        const userInput = userInputField.value.trim();
        if (userInput) {
            // Si LEAN BOT está disponible, usar solo el backend
            if (window.leanBotAPI && window.leanBotAPI.isBackendAvailable) {
                // Mostrar mensaje del usuario inmediatamente con estilos correctos
                const userMessage = document.createElement("div");
                userMessage.classList.add("message", "user-message");
                userMessage.innerHTML = `
                    <div class="message-avatar user-avatar">
                        <span>U</span>
                    </div>
                    <div class="message-content">
                        <div class="message-text">${userInput}</div>
                        <div class="message-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                `;
                chatWindow.appendChild(userMessage);

                // Mostrar indicador de carga
                const loadingIndicator = document.createElement("div");
                loadingIndicator.classList.add("message", "bot-message");
                loadingIndicator.innerHTML = `
                    <div class="message-avatar bot-avatar">
                        <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                    </div>
                    <div class="message-content">
                        <div class="message-text">
                            <span class="loading"></span> Procesando...
                        </div>
                        <div class="message-time">${new Date().toLocaleTimeString()}</div>
                    </div>
                `;
                chatWindow.appendChild(loadingIndicator);
                
                // Desplazarse al final del chat
                chatWindow.scrollTop = chatWindow.scrollHeight;
                
                try {
                    // Enviar al backend y obtener respuesta
                    const fullResponse = await window.leanBotAPI.sendMessage(userInput);
                    
                    // Reemplazar indicador de carga con la respuesta del backend
                    chatWindow.removeChild(loadingIndicator);
                    
                    const botMessage = document.createElement("div");
                    botMessage.classList.add("message", "bot-message");
                    botMessage.innerHTML = `
                        <div class="message-avatar bot-avatar">
                            <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                        </div>
                        <div class="message-content">
                            <div class="message-text">${fullResponse.response || fullResponse}</div>
                            <div class="message-time">${new Date().toLocaleTimeString()}</div>
                        </div>
                    `;
                    chatWindow.appendChild(botMessage);
                    
                } catch (error) {
                    console.error('❌ Error con backend:', error);
                    // Reemplazar indicador de carga con mensaje de error
                    chatWindow.removeChild(loadingIndicator);
                    
                    const errorMessage = document.createElement("div");
                    errorMessage.classList.add("message", "bot-message");
                    errorMessage.innerHTML = `
                        <div class="message-avatar bot-avatar">
                            <img src="img/Favicon.png" alt="Bot" width="40" height="40" />
                        </div>
                        <div class="message-content">
                            <div class="message-text">Lo siento, tengo problemas de conectividad. ¿Podrías intentarlo más tarde?</div>
                            <div class="message-time">${new Date().toLocaleTimeString()}</div>
                        </div>
                    `;
                    chatWindow.appendChild(errorMessage);
                }
            } else {
                // Fallback: usar sistema local (sin estilos para distinguir)
                const userMessage = document.createElement("div");
                userMessage.classList.add("user-message");
                userMessage.textContent = userInput;
                chatWindow.appendChild(userMessage);

                // Mostrar indicador de carga
                const loadingIndicator = document.createElement("div");
                loadingIndicator.classList.add("bot-message");
                loadingIndicator.innerHTML = '<span class="loading"></span> Procesando...';
                chatWindow.appendChild(loadingIndicator);
                
                // Desplazarse al final del chat
                chatWindow.scrollTop = chatWindow.scrollHeight;

                // Obtener respuesta del bot local
                const botResponse = await getBotResponse(userInput);
                
                // Reemplazar indicador de carga con la respuesta
                chatWindow.removeChild(loadingIndicator);
                
                const botMessage = document.createElement("div");
                botMessage.classList.add("bot-message");
                botMessage.textContent = botResponse;
                chatWindow.appendChild(botMessage);
            }

            userInputField.value = ""; // Limpiar campo de entrada
            chatWindow.scrollTop = chatWindow.scrollHeight; // Desplazarse al final
        }
    }

    // Evento de click para el botón de enviar
    chatButton.addEventListener("click", sendMessage);

    // Evento de tecla para permitir enviar con Enter
    userInputField.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
    
    // Integración con reconocimiento de voz
    if (window.voiceRecognition) {
        // Agregar evento para enviar automáticamente después de reconocer la voz
        if (window.SpeechRecognition || window.webkitSpeechRecognition) {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.onresult = function(event) {
                userInputField.value = event.results[0][0].transcript;
                // Pequeña pausa antes de enviar para que el usuario vea lo que se reconoció
                setTimeout(sendMessage, 500);
            };
            
            // Reemplazar el evento click del micrófono
            micButton.addEventListener("click", function() {
                if (window.voiceRecognition) {
                    window.voiceRecognition.toggle();
                }
            });
        }
    }
});