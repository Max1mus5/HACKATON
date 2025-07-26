import os
import requests

def analizar_sentimiento_gemini(texto):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise Exception("API key de Gemini no configurada en variables de entorno.")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    prompt = (
        "Eres un analizador de sentimientos profesional. "
        "Analiza el sentimiento del siguiente texto y responde únicamente con una de estas palabras: positivo, negativo o neutro. "
        "No expliques tu respuesta, solo responde con la palabra correspondiente.\n\n"
        f"Texto: {texto}"
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
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    # Extraer la respuesta del modelo
    sentimiento = result["candidates"][0]["content"]["parts"][0]["text"].strip().lower()
    return sentimiento
