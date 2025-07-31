"""
Vercel Serverless Function para LEAN BOT API
Este archivo sirve como punto de entrada para el backend en Vercel
"""
import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configurar variables de entorno para Vercel
if not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0"

# Crear aplicación FastAPI simple para Vercel
app = FastAPI(title="LEAN BOT API - Vercel", description="API simplificada para Vercel")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints básicos para pruebas
@app.get("/")
def health_check():
    return {"status": "ok", "message": "LEAN BOT API funcionando en Vercel"}

@app.get("/sentiment/model-info")
def get_sentiment_model_info():
    """
    Información del modelo de análisis de sentimientos (versión simplificada)
    """
    return {
        "model_name": "finiteautomata/beto-sentiment-analysis",
        "available": False,
        "reason": "Dependencias no disponibles en Vercel",
        "fallback": "Análisis básico disponible",
        "confidence": 0.0,
        "labels": ["POS", "NEG", "NEU"]
    }

@app.get("/analytics/dashboard")
def get_sentiment_dashboard():
    """
    Dashboard de análisis de sentimientos (datos de ejemplo)
    """
    return {
        "total_messages": 0,
        "avg_confidence": 0.0,
        "positive_ratio": 0.33,
        "negative_ratio": 0.33,
        "neutral_ratio": 0.34,
        "metrics_24h": {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "avg_confidence": 0.0
        },
        "metrics_week": {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "avg_confidence": 0.0
        },
        "hourly_trends": [],
        "sentiment_keywords": {
            "positive": [],
            "negative": [],
            "neutral": []
        },
        "active_conversations": []
    }

@app.post("/sentiment/analyze")
def analyze_sentiment(request: dict):
    """
    Análisis de sentimiento básico (sin BETO)
    """
    text = request.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Texto requerido")
    
    # Análisis básico por palabras clave
    positive_words = ["bueno", "excelente", "genial", "perfecto", "increíble", "fantástico"]
    negative_words = ["malo", "terrible", "horrible", "pésimo", "awful", "odio"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "POS"
        confidence = min(0.8, 0.5 + positive_count * 0.1)
    elif negative_count > positive_count:
        sentiment = "NEG"
        confidence = min(0.8, 0.5 + negative_count * 0.1)
    else:
        sentiment = "NEU"
        confidence = 0.6
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "label": {"POS": "Positivo", "NEG": "Negativo", "NEU": "Neutral"}[sentiment]
    }

# Intentar importar la aplicación completa como fallback
try:
    # Agregar el directorio src/Backend al path de Python
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'Backend'))
    
    from api import app as full_app
    print("✅ Aplicación completa importada exitosamente")
    app = full_app
except Exception as e:
    print(f"⚠️ Usando aplicación simplificada: {e}")
    # Mantener la aplicación simplificada definida arriba
