import os
import requests

def analizar_sentimiento_gemini(texto, api_key=None):
    """
    Analiza el sentimiento de un texto usando Gemini API
    """
    # Usar la API key proporcionada o la del entorno
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAel_ApU1CspuRaeqT0Z6jc0CblthtMlbE")
    
    if not api_key:
        raise Exception("API key de Gemini no configurada.")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    prompt = (
        "Eres un analizador de sentimientos profesional para LEAN BOT de INGE LEAN. "
        "Analiza el sentimiento del siguiente mensaje del usuario y responde únicamente con una de estas palabras: positivo, negativo o neutro. "
        "Considera el contexto de una conversación con un chatbot empresarial. "
        "No expliques tu respuesta, solo responde con la palabra correspondiente.\n\n"
        f"Mensaje del usuario: {texto}"
    )
    
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 10,
            "topP": 0.95
        }
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Extraer la respuesta del modelo
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                sentimiento = candidate["content"]["parts"][0]["text"].strip().lower()
                return sentimiento
            else:
                return "neutro"  # Default si no hay respuesta válida
        else:
            return "neutro"  # Default si no hay candidatos
            
    except requests.exceptions.Timeout:
        print("Timeout en análisis de sentimiento")
        return "neutro"
    except requests.exceptions.RequestException as e:
        print(f"Error en petición de análisis de sentimiento: {e}")
        return "neutro"
    except Exception as e:
        print(f"Error inesperado en análisis de sentimiento: {e}")
        return "neutro"
