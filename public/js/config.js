// Archivo de configuración para claves API y otras configuraciones sensibles
// IMPORTANTE: Este archivo no debe incluirse en el control de versiones (añádelo a .gitignore)

const API_CONFIG = {
    // Usar variable de entorno si está disponible, sino usar API key por defecto
    geminiApiKey: typeof process !== 'undefined' && process.env && process.env.GEMINI_API_KEY 
        ? process.env.GEMINI_API_KEY 
        : "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0"
};
