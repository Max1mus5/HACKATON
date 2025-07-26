#!/usr/bin/env python3
"""
Script de inicio para LEAN BOT Backend
"""
import os
import sys
import subprocess

def main():
    """Función principal para iniciar el servidor LEAN BOT"""
    
    print("🤖 Iniciando LEAN BOT Backend...")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    backend_dir = os.path.join(os.path.dirname(__file__), "src", "Backend")
    
    if not os.path.exists(backend_dir):
        print("❌ Error: No se encontró el directorio del backend")
        sys.exit(1)
    
    # Cambiar al directorio del backend
    os.chdir(backend_dir)
    
    # Verificar si uvicorn está instalado
    try:
        subprocess.run(["uvicorn", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: uvicorn no está instalado")
        print("💡 Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    # Configurar variables de entorno si no existen
    if not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "AIzaSyAel_ApU1CspuRaeqT0Z6jc0CblthtMlbE"
        print("🔑 API Key de Gemini configurada automáticamente")
    
    print("✅ Configuración completada")
    print("🚀 Iniciando servidor en http://localhost:8000")
    print("📚 Documentación API en http://localhost:8000/docs")
    print("🔄 Para detener el servidor, presiona Ctrl+C")
    print("=" * 50)
    
    try:
        # Iniciar el servidor uvicorn
        subprocess.run([
            "uvicorn", 
            "api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor LEAN BOT detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
