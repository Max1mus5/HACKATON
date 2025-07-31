#!/usr/bin/env python3
"""
Punto de entrada principal para LEAN BOT
Ejecuta el servidor FastAPI con todas las configuraciones necesarias
"""

import sys
import os
import uvicorn

# Agregar el directorio src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Configurar variables de entorno por defecto
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0"
    
    print("🚀 Iniciando LEAN BOT Server...")
    print("📊 Sistema de análisis de sentimientos con BETO activado")
    print("🔗 Endpoints disponibles:")
    print("   - Chat: http://localhost:12000/chat.html")
    print("   - Analytics: http://localhost:12000/analytics.html")
    print("   - API Docs: http://localhost:12000/docs")
    print("   - Dashboard: http://localhost:12000/dashboard.html")
    
    # Ejecutar el servidor
    uvicorn.run(
        "Backend.api:app",
        host="0.0.0.0",
        port=12000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )