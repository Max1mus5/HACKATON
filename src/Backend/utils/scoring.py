"""
Módulo para cálculo de scores de mensajes usando IA (Gemini o Mistral)
"""

import os
import requests
import json
from src.Backend.utils.gemini_sentiment import analizar_sentimiento_gemini

def calculate_message_score(mensaje_usuario, respuesta_bot, ai_provider="gemini", api_key=None):
    """
    Calcula el score de un mensaje usando IA (Gemini o Mistral) con contexto completo.
    
    Args:
        mensaje_usuario (str): El mensaje del usuario
        respuesta_bot (str): La respuesta generada por el bot
        ai_provider (str): Proveedor de IA a usar ("gemini" o "mistral")
        api_key (str): API key personalizada (opcional)
        
    Returns:
        float: Score entre 1.0 y 10.0
    """
    try:
        # Usar el servicio unificado de IA
        from ..utils.ai_chat_service import AIChatService
        
        ai_service = AIChatService()
        
        # Si no se proporciona API key personalizada, usar la configuración por defecto
        if not api_key and ai_provider == "gemini":
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
        
        # Usar el servicio unificado de IA para generar el score
        ai_result = ai_service.generate_response(
            prompt,
            conversation_history=[],
            provider=ai_provider,
            api_key=api_key
        )
        
        if ai_result["success"]:
            score_text = ai_result["response"].strip()
            # Extraer solo el número
            import re
            score_match = re.search(r'\b([1-9]|10)\b', score_text)
            if score_match:
                score = float(score_match.group(1))
                print(f"✅ Score calculado por {ai_provider}: {score} para mensaje: '{mensaje_usuario[:50]}...'")
                return score
            else:
                print(f"⚠️ No se pudo extraer score de respuesta {ai_provider}: {score_text}")
        
        # Fallback: usar análisis de sentimiento básico
        print("⚠️ Usando fallback de análisis de sentimiento")
        if ai_provider == "gemini":
            sentimiento = analizar_sentimiento_gemini(mensaje_usuario)
        else:
            # Para Mistral, usar análisis básico de palabras clave
            sentimiento = analyze_sentiment_basic(mensaje_usuario)
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

def analyze_sentiment_basic(mensaje):
    """
    Análisis básico de sentimientos usando palabras clave
    """
    mensaje_lower = mensaje.lower()
    
    # Palabras positivas
    palabras_positivas = [
        'gracias', 'excelente', 'perfecto', 'genial', 'bueno', 'bien', 'fantástico',
        'increíble', 'maravilloso', 'estupendo', 'feliz', 'contento', 'satisfecho',
        'me gusta', 'me encanta', 'amor', 'positivo', 'sí', 'correcto', 'exacto'
    ]
    
    # Palabras negativas
    palabras_negativas = [
        'malo', 'terrible', 'horrible', 'pésimo', 'odio', 'detesto', 'no me gusta',
        'problema', 'error', 'falla', 'incorrecto', 'mal', 'negativo', 'no', 'nunca',
        'imposible', 'difícil', 'complicado', 'frustrado', 'molesto', 'enojado'
    ]
    
    # Contar palabras positivas y negativas
    positivas = sum(1 for palabra in palabras_positivas if palabra in mensaje_lower)
    negativas = sum(1 for palabra in palabras_negativas if palabra in mensaje_lower)
    
    if positivas > negativas:
        return "positivo"
    elif negativas > positivas:
        return "negativo"
    else:
        return "neutro"