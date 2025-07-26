
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

// Cargar la clave API desde localStorage si existe
document.addEventListener("DOMContentLoaded", function() {
    // Cargar clave desde localStorage si está disponible
    const savedApiKey = localStorage.getItem('gemini_api_key');
    if (savedApiKey) {
        config.geminiAPIKey = savedApiKey;
        console.log("Clave API cargada desde almacenamiento local");
    }
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
    // Primero, intentar usar LEAN BOT API si está disponible
    if (window.leanBotAPI && window.leanBotAPI.isBackendAvailable) {
        try {
            console.log('🤖 Usando LEAN BOT backend para respuesta...');
            const fullResponse = await window.leanBotAPI.sendMessage(userInput);
            
            // Si es una respuesta del backend, retornar la respuesta del bot
            if (fullResponse && fullResponse.response && !fullResponse.fallback) {
                console.log('✅ Respuesta de LEAN BOT obtenida');
                return fullResponse.response;
            }
        } catch (error) {
            console.error('❌ Error con LEAN BOT backend, usando fallback local:', error);
        }
    }

    // Fallback al sistema local original si LEAN BOT no está disponible
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
    const userInputField = document.getElementById("user-input");
    const chatButton = document.getElementById("chat-button");
    const chatWindow = document.getElementById("chat-window");
    const micButton = document.getElementById("mic-button");
    
    // Elementos para el modal de configuración
    const settingsButton = document.getElementById("settings-button");
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
        apiKeyInput.value = localStorage.getItem('gemini_api_key');
    }
    
    if (localStorage.getItem('gemini_model')) {
        geminiModelSelect.value = localStorage.getItem('gemini_model');
    }
    
    // Abrir modal de configuración
    settingsButton.onclick = function() {
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
    saveApiSettings.onclick = function() {
        const apiKey = apiKeyInput.value.trim();
        const modelName = geminiModelSelect.value;
        
        // Guardar en localStorage
        localStorage.setItem('gemini_api_key', apiKey);
        localStorage.setItem('gemini_model', modelName);
        
        // Actualizar configuración
        config.geminiAPIKey = apiKey;
        config.geminiModel = modelName;
        config.apiTested = false; // Forzar nueva prueba con la nueva configuración
        
        // Mostrar mensaje de éxito
        apiTestResult.innerHTML = "Configuración guardada correctamente.";
        apiTestResult.className = "mt-3 success";
        
        // Mostrar mensaje en el chat
        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");
        botMessage.textContent = "La configuración de la API de Gemini ha sido actualizada.";
        chatWindow.appendChild(botMessage);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        
        // Cerrar modal después de un momento
        setTimeout(() => {
            settingsModal.style.display = "none";
        }, 1500);
    }
    
    // Probar conexión con la API
    testApiConnection.onclick = async function() {
        const apiKey = apiKeyInput.value.trim();
        const modelName = geminiModelSelect.value;
        
        if (!apiKey) {
            apiTestResult.innerHTML = "Por favor, ingresa una clave API válida.";
            apiTestResult.className = "mt-3 error";
            return;
        }
        
        // Mostrar cargando
        apiTestResult.innerHTML = "Probando conexión...";
        apiTestResult.className = "mt-3";
        
        // Actualizar configuración temporalmente
        const originalKey = config.geminiAPIKey;
        const originalModel = config.geminiModel;
        
        try {
            config.geminiAPIKey = apiKey;
            config.geminiModel = modelName;
            config.apiTested = false;
            
            const success = await testGeminiAPI();
            
            if (success) {
                apiTestResult.innerHTML = "¡Conexión exitosa! La API de Gemini está funcionando correctamente.";
                apiTestResult.className = "mt-3 success";
            } else {
                apiTestResult.innerHTML = "No se pudo conectar con la API de Gemini. Verifica tu clave API.";
                apiTestResult.className = "mt-3 error";
                
                // Restaurar configuración original si la prueba falla
                config.geminiAPIKey = originalKey;
                config.geminiModel = originalModel;
            }
        } catch (error) {
            console.error("Error al probar API:", error);
            apiTestResult.innerHTML = "Error al probar la conexión: " + error.message;
            apiTestResult.className = "mt-3 error";
            
            // Restaurar configuración original si hay un error
            config.geminiAPIKey = originalKey;
            config.geminiModel = originalModel;
        }
    }

    // Función para enviar mensaje
    async function sendMessage() {
        const userInput = userInputField.value;
        if (userInput) {
            const userMessage = document.createElement("div");
            userMessage.classList.add("user-message");
            userMessage.textContent = userInput;
            chatWindow.appendChild(userMessage);

            // Mostrar indicador de carga mientras se procesa la respuesta
            const loadingIndicator = document.createElement("div");
            loadingIndicator.classList.add("bot-message");
            loadingIndicator.innerHTML = '<span class="loading"></span> Procesando...';
            chatWindow.appendChild(loadingIndicator);
            
            // Desplazarse al final del chat
            chatWindow.scrollTop = chatWindow.scrollHeight;

            // Obtener respuesta del bot
            const botResponse = await getBotResponse(userInput);
            
            // Reemplazar indicador de carga con la respuesta
            chatWindow.removeChild(loadingIndicator);
            
            const botMessage = document.createElement("div");
            botMessage.classList.add("bot-message");
            botMessage.textContent = botResponse;
            chatWindow.appendChild(botMessage);

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