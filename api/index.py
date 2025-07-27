"""
Vercel Serverless Function para LEAN BOT API
Este archivo sirve como punto de entrada para el backend en Vercel
"""
import sys
import os

# Agregar el directorio src/Backend al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'Backend'))

# Importar la aplicación FastAPI
try:
    from api import app
except ImportError:
    # Fallback para estructura alternativa
    import importlib.util
    api_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'Backend', 'api.py')
    spec = importlib.util.spec_from_file_location("api", api_path)
    api_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api_module)
    app = api_module.app

# Configurar variables de entorno para Vercel
if not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0"

# Función handler para Vercel
def handler(request, response):
    """
    Handler principal para las peticiones de Vercel
    """
    return app

# Exportar la aplicación para Vercel
# Vercel buscará automáticamente 'app' o 'handler'
app = app
