"""
Módulo para cálculo de scores de mensajes usando Gemini AI
"""

import os
import requests
import json
from utils.gemini_sentiment import analizar_sentimiento_gemini

def calculate_message_score(mensaje_usuario, respuesta_bot):
    """
    Calcula el score de un mensaje usando Gemini AI con contexto completo.
    
    Args:
        mensaje_usuario (str): El mensaje del usuario
        respuesta_bot (str): La respuesta generada por el bot
        
    Returns:
        float: Score entre 1.0 y 10.0
    """
    try:
        # Obtener API key desde variable de entorno o runtime
        api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0")
        
        # Intentar obtener desde variable global si existe
        try:
            import sys
            if 'src.Backend.api' in sys.modules:
                api_module = sys.modules['src.Backend.api']
                if hasattr(api_module, 'GEMINI_API_KEY_RUNTIME') and api_module.GEMINI_API_KEY_RUNTIME:
                    api_key = api_module.GEMINI_API_KEY_RUNTIME
        except:
            pass
        
        if not api_key:
            print("⚠️ No se encontró API key de Gemini, usando fallback")
            raise Exception("No API key available")
        
        # Prompt mejorado para análisis de score con contexto completo
        prompt = f"""
Analiza la siguiente conversación y asigna un score del 1 al 10 basado en:
- Sentimiento del usuario (positivo=7-10, neutral=4-6, negativo=1-3)
- Calidad de la interacción
- Satisfacción aparente del usuario
- Contexto de la conversación

Usuario: "{mensaje_usuario}"
Bot: "{respuesta_bot}"

Responde SOLO con un número del 1 al 10, sin explicaciones.
"""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 10
            }
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    score_text = candidate["content"]["parts"][0]["text"].strip()
                    # Extraer solo el número
                    import re
                    score_match = re.search(r'\b([1-9]|10)\b', score_text)
                    if score_match:
                        score = float(score_match.group(1))
                        print(f"✅ Score calculado por Gemini: {score} para mensaje: '{mensaje_usuario[:50]}...'")
                        return score
                    else:
                        print(f"⚠️ No se pudo extraer score de respuesta Gemini: {score_text}")
        
        # Fallback: usar análisis de sentimiento básico
        print("⚠️ Usando fallback de análisis de sentimiento")
        sentimiento = analizar_sentimiento_gemini(mensaje_usuario)
        if sentimiento == "positivo":
            score = 7.0
        elif sentimiento == "negativo":
            score = 3.0
        else:  # neutro
            score = 5.0
        
        print(f"⚠️ Score calculado con fallback: {score}")
        return score
            
    except Exception as e:
        print(f"Error calculando score con Gemini: {e}")
        # Fallback: usar análisis de sentimiento básico
        try:
            sentimiento = analizar_sentimiento_gemini(mensaje_usuario)
            if sentimiento == "positivo":
                return 7.0
            elif sentimiento == "negativo":
                return 3.0
            else:
                return 5.0
        except:
            return 5.0  # Score neutral por defecto