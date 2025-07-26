"""
Servidor de desarrollo para la API de LEAN Chatbot
"""
import uvicorn
from api import app

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=True,
        log_level="debug"
    )
