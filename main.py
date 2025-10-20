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
    # Verificar y configurar API key con el gestor
    from Backend.utils.api_key_manager import get_working_api_key

    try:
        # Intentar obtener una API key funcional
        active_key = get_working_api_key()
        print(f"✅ API key funcional encontrada: {active_key[:15]}...")
    except ValueError as e:
        print(f"⚠️  Advertencia: {e}")
        print("   El servidor iniciará, pero las funciones de IA pueden no estar disponibles.")

    print("\n🚀 Iniciando LEAN BOT Server...")
    print("📊 Sistema de análisis de sentimientos con BETO activado")
    print("🤖 Sistema de múltiples API keys con fallback automático")
    print("\n🔗 Endpoints disponibles:")
    print("   - Chat: http://localhost:PORT/chat.html")
    print("   - Analytics: http://localhost:PORT/analytics.html")
    print("   - API Docs: http://localhost:PORT/docs")
    print("   - Dashboard: http://localhost:PORT/dashboard.html")
    print("\n" + "="*60)

    # Ejecutar el servidor SIEMPRE en el puerto 8000 (coherente con Render)
    uvicorn.run(
        "Backend.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )