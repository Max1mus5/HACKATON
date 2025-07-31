// Configuración de entorno para LEAN BOT Frontend
const ENV_CONFIG = {
    // URL base del backend - cambiar según el entorno
    BASE_URL: "https://hackaton-d1h6.onrender.com",
    
    // URLs específicas para diferentes entornos
    DEVELOPMENT: {
        BASE_URL: "http://localhost:8000"
    },
    
    PRODUCTION: {
        BASE_URL: "https://hackaton-d1h6.onrender.com"
    },
    
    // Detectar automáticamente el entorno
    getBaseURL: function() {
        // Detectar si estamos en Vercel o desarrollo local
        if (window.location.hostname.includes('vercel.app')) {
            // En Vercel, usar rutas relativas
            const baseURL = window.location.origin;
            console.log('🌐 ENV_CONFIG: Usando Vercel:', baseURL);
            return baseURL;
        } else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            // En desarrollo local
            const baseURL = "http://localhost:8000";
            console.log('🌐 ENV_CONFIG: Usando desarrollo local:', baseURL);
            return baseURL;
        } else {
            // Fallback a Render
            const baseURL = "https://hackaton-d1h6.onrender.com";
            console.log('🌐 ENV_CONFIG: Usando Render fallback:', baseURL);
            return baseURL;
        }
    },
    
    // Configuración adicional
    API_ENDPOINTS: {
        HEALTH: "/",
        CONFIG_API_KEY: "/config/gemini_api_key",
        USERS: "/usuarios/",
        USER_MESSAGES: "/usuarios/{doc_id}/messages",
        USER_MESSAGE: "/usuarios/{doc_id}/message",
        CHAT_MESSAGES: "/chats/{chat_id}/messages",
        CHAT_SCORE: "/chats/{chat_id}/score",
        ALL_CHATS: "/chats/",
        TEST_GEMINI: "/test/gemini"
    },
    
    // Timeout para requests
    REQUEST_TIMEOUT: 30000,
    
    // Configuración de logs
    DEBUG_MODE: false // Desactivado para producción
};

// Hacer disponible globalmente
window.ENV_CONFIG = ENV_CONFIG;

// Log de configuración
console.log('🔧 ENV_CONFIG cargado:', {
    baseURL: ENV_CONFIG.getBaseURL(),
    environment: 'PRODUCTION',
    debugMode: ENV_CONFIG.DEBUG_MODE
});
