import requests
import json
import os
from typing import Dict, Any

class GeminiChatService:
    def __init__(self, api_key: str = None):
        # Priorizar la API key en este orden: parámetro > variable global > variable de entorno
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = "gemini-1.5-flash-latest"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        # Contexto base de LEAN BOT
        self.lean_context = """
        Eres LEAN BOT, un asistente virtual de la empresa INGE LEAN. Tu personalidad es amigable, profesional y siempre dispuesto a ayudar.
        
        Información sobre INGE LEAN:
        - Es una empresa de ingeniería especializada en consultoría y desarrollo de proyectos.
        - Ofrece servicios de consultoría técnica, desarrollo de software y soluciones tecnológicas.
        - Se enfoca en metodologías ágiles y lean para optimizar procesos.
        - Tiene un equipo multidisciplinario de ingenieros y desarrolladores.
        
        Como LEAN BOT debes:
        - Presentarte como el asistente virtual de INGE LEAN
        - Ser cordial y profesional en todas tus respuestas
        - Proporcionar información útil sobre la empresa cuando sea apropiado
        - Mantener respuestas concisas pero informativas
        - Siempre estar dispuesto a ayudar con consultas técnicas o generales
        
        Responde de manera natural y conversacional, como si fueras un miembro del equipo de INGE LEAN.
        """
    
    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Genera una respuesta usando Gemini API con el contexto de LEAN BOT
        """
        try:
            # Verificar que tenemos una API key disponible
            current_api_key = self.api_key or os.getenv("GEMINI_API_KEY")
            if not current_api_key:
                return "Lo siento, no tengo configurada la conexión con el servicio de chat. Por favor, configura la API key."
            
            # Construir el prompt completo con contexto
            messages = [{"text": self.lean_context}]
            
            # Agregar historial de conversación si existe
            if conversation_history:
                for msg in conversation_history[-5:]:  # Últimos 5 mensajes para contexto
                    if isinstance(msg, dict):
                        if msg.get("message"):
                            messages.append({"text": f"Usuario: {msg['message']}"})
                        if msg.get("response"):
                            messages.append({"text": f"LEAN BOT: {msg['response']}"})
            
            # Agregar el mensaje actual del usuario
            messages.append({"text": f"Usuario: {user_message}\n\nResponde como LEAN BOT:"})
            
            # Preparar la petición a Gemini
            data = {
                "contents": [
                    {
                        "parts": messages
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 300,
                    "topP": 0.95,
                    "topK": 40
                }
            }
            
            # Hacer la petición a Gemini API
            response = requests.post(
                f"{self.base_url}?key={current_api_key}",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extraer la respuesta del modelo
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    bot_response = candidate["content"]["parts"][0]["text"].strip()
                    return bot_response
                else:
                    return "Lo siento, no pude generar una respuesta en este momento."
            else:
                return "Lo siento, no pude procesar tu mensaje. ¿Podrías intentarlo de nuevo?"
                
        except requests.exceptions.Timeout:
            return "Lo siento, la respuesta está tomando más tiempo del esperado. ¿Podrías intentarlo de nuevo?"
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición a Gemini: {e}")
            return "Lo siento, tengo problemas de conectividad. ¿Podrías intentarlo más tarde?"
        except Exception as e:
            print(f"Error inesperado en Gemini Chat Service: {e}")
            return "Lo siento, algo salió mal. ¿Podrías intentarlo de nuevo?"
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con Gemini API
        """
        try:
            test_response = self.generate_response("Hola, ¿funcionas correctamente?")
            return test_response is not None and "Lo siento" not in test_response
        except:
            return False
