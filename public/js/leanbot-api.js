// Configuración para LEAN BOT integrado con backend
class LeanBotAPI {
    constructor() {
        // Detectar automáticamente la URL base según el entorno
        this.baseURL = this.getBaseURL();
        this.currentUserId = this.getUserId();
        this.currentChatId = null;
        this.isBackendAvailable = false;
        this.checkBackendAvailability();
    }

    // Detectar la URL base según el entorno
    getBaseURL() {
        // Backend URL hardcodeado apuntando a Render
        const baseURL = 'https://hackaton-d1h6.onrender.com';
        console.log('🌐 Usando BASE_URL hardcodeado:', baseURL);
        return baseURL;
    }

    // Generar o recuperar ID de usuario único
    getUserId() {
        let userId = localStorage.getItem('lean_bot_user_id');
        if (!userId) {
            userId = Date.now(); // Usar timestamp como ID único simple
            localStorage.setItem('lean_bot_user_id', userId);
        }
        return parseInt(userId);
    }

    // Verificar si el backend está disponible
    async checkBackendAvailability() {
        try {
            const response = await fetch(`${this.baseURL}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.isBackendAvailable = true;
                console.log('✅ Backend LEAN BOT disponible:', data.message);
                await this.initializeUser();
            } else {
                throw new Error('Backend no responde correctamente');
            }
        } catch (error) {
            console.warn('⚠️ Backend LEAN BOT no disponible:', error.message);
            this.isBackendAvailable = false;
        }
    }

    // Inicializar usuario en el backend
    async initializeUser() {
        try {
            const response = await fetch(`${this.baseURL}/usuarios/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    doc_id: this.currentUserId
                })
            });

            if (response.ok) {
                const userData = await response.json();
                this.currentChatId = userData.chat.id;
                console.log('✅ Usuario inicializado:', userData);
                return userData;
            } else {
                throw new Error('No se pudo inicializar usuario');
            }
        } catch (error) {
            console.error('❌ Error al inicializar usuario:', error);
            this.isBackendAvailable = false;
            return null;
        }
    }

    // Enviar mensaje al backend con LEAN BOT
    async sendMessage(userMessage) {
        if (!this.isBackendAvailable || !this.currentChatId) {
            console.warn('Backend no disponible, usando fallback local');
            return this.fallbackResponse(userMessage);
        }

        try {
            const response = await fetch(`${this.baseURL}/usuarios/${this.currentUserId}/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    timestamp: new Date().toISOString()
                })
            });

            if (response.ok) {
                const messageData = await response.json();
                console.log('✅ Respuesta del backend:', messageData);
                return messageData;
            } else {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('❌ Error al enviar mensaje:', error);
            return this.fallbackResponse(userMessage);
        }
    }

    // Respuesta de fallback cuando el backend no está disponible
    fallbackResponse(userMessage) {
        const fallbackResponses = [
            "Hola, soy LEAN BOT de INGE LEAN. Actualmente estoy en modo offline, pero pronto estaré completamente disponible.",
            "Gracias por tu mensaje. LEAN BOT está temporalmente en mantenimiento. ¿Podrías intentarlo más tarde?",
            "Soy el asistente virtual de INGE LEAN. En este momento tengo conectividad limitada, pero estaré disponible pronto."
        ];

        const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
        
        return {
            message: userMessage,
            response: randomResponse,
            score: 5.0,
            timestamp: new Date().toISOString(),
            fallback: true
        };
    }

    // Obtener historial del chat
    async getChatHistory() {
        if (!this.isBackendAvailable || !this.currentUserId) {
            return [];
        }

        try {
            // Usar el nuevo endpoint que devuelve solo los mensajes
            const response = await fetch(`${this.baseURL}/usuarios/${this.currentUserId}/messages`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                console.log('📋 Historial obtenido:', data.mensajes ? data.mensajes.length : 0, 'mensajes');
                return data.mensajes || [];
            } else {
                console.warn('No se pudo obtener historial del chat');
                return [];
            }
        } catch (error) {
            console.error('Error al obtener historial:', error);
            return [];
        }
    }

    // Probar conexión con Gemini
    async testGeminiConnection() {
        try {
            const response = await fetch(`${this.baseURL}/test/gemini`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const result = await response.json();
                console.log('🤖 Estado de Gemini:', result);
                return result;
            } else {
                return { status: 'error', message: 'No se pudo probar Gemini' };
            }
        } catch (error) {
            console.error('Error al probar Gemini:', error);
            return { status: 'error', message: error.message };
        }
    }

    // Obtener estadísticas del chat
    async getChatStats() {
        if (!this.isBackendAvailable || !this.currentChatId) {
            return null;
        }

        try {
            const response = await fetch(`${this.baseURL}/chats/${this.currentChatId}/score`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const scoreData = await response.json();
                return scoreData;
            } else {
                return null;
            }
        } catch (error) {
            console.error('Error al obtener estadísticas:', error);
            return null;
        }
    }
}

// Inicializar la API de LEAN BOT
const leanBotAPI = new LeanBotAPI();

// Función global para integrar con el chatbot existente
async function getLeanBotResponse(userMessage) {
    const response = await leanBotAPI.sendMessage(userMessage);
    return response.response;
}

// Función para obtener respuesta completa con metadatos
async function getLeanBotFullResponse(userMessage) {
    return await leanBotAPI.sendMessage(userMessage);
}

// Función para mostrar información de LEAN BOT en consola
window.leanBotInfo = function() {
    console.log(`
🤖 LEAN BOT - Asistente Virtual de INGE LEAN
===============================================
Estado del Backend: ${leanBotAPI.isBackendAvailable ? '✅ Conectado' : '❌ Desconectado'}
Usuario ID: ${leanBotAPI.currentUserId}
Chat ID: ${leanBotAPI.currentChatId || 'No disponible'}
URL Backend: ${leanBotAPI.baseURL}

Funciones disponibles:
- leanBotAPI.sendMessage(mensaje)
- leanBotAPI.getChatHistory()
- leanBotAPI.testGeminiConnection()
- leanBotAPI.getChatStats()
===============================================
    `);
};

// Mostrar información al cargar
console.log('🤖 LEAN BOT iniciado. Usa leanBotInfo() para más información.');

// Exportar la instancia para uso global
window.leanBotAPI = leanBotAPI;
