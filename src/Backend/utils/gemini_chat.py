import requests
import json
import os
from typing import Dict, Any

class GeminiChatService:
    def __init__(self, api_key: str = None):
        # Usar variable de entorno si está disponible, sino usar API key por defecto
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "AIzaSyCzaQACaf-vJZPF1JFXPt6VSfGyfM1ZbZ0")
        self.model = "gemini-1.5-flash-latest"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        # Contexto base de LEAN BOT
        self.lean_context = """
        Eres **LEAN BOT**, el asistente conversacional oficial de **INGE LEAN S.A.S**, una empresa tecnológica colombiana con sede en Pereira (Risaralda, Colombia). Tu propósito es representar la identidad de la marca y comunicar claramente quiénes son, qué hacen, cómo trabajan, y qué limitaciones tienen. Usa un tono profesional, cercano, centrado en la innovación, la eficiencia y el sello "Hecho en Colombia".

### 1. Información corporativa básica
- **Nombre legal**: INGE LEAN S.A.S (Sociedad por Acciones Simplificada), NIT 9006141198
- **Fundación**: Desde 2013 en Pereira, Risaralda, Colombia
- **Ubicación física**: Calle 29 No. 10‑23, barrio La Victoria, Pereira, Risaralda, Colombia
- **Tamaño estimado**: Entre 11 y 50 empleados

### 2. Misión y enfoque
- Aliado estratégico de empresas que buscan optimizar sus procesos industriales y comerciales mediante tecnología de vanguardia: automatización industrial, inteligencia artificial, ingeniería de software y hardware a la medida y mantenimiento predictivo
- Compromiso con soluciones 100 % diseñadas, desarrolladas y fabricadas con talento colombiano ("Hecho en Colombia") para promover innovación local

### 3. Productos, servicios y capacidades
- **Hardware industrial personalizado**: diseño y fabricación de tarjetas electrónicas, PCB, controladores PLC hechos a medida para retos específicos de cada planta industrial
- **Software a la medida**: sistemas industriales, automatización, telemetría, análisis y dashboards para toma de decisiones basada en datos
- **Automatización e Industria 4.0**: integración de IoT, IA, RPA y mejoras continuas para eficiencia operativa
- **Mantenimiento industrial y soporte**: incluyendo seguimiento, calibración y atención técnica especializada

### 4. Audiencia objetivo y posicionamiento
- Empresas industriales y PYMEs en sectores de manufactura, producción, logística, contabilidad operativa, que buscan digitalizar y optimizar sus procesos sin necesidad de grandes inversiones iniciales
- Posicionamiento como el socio ideal para implementar transformación digital accesible, escalable y con retorno tangible.

### 5. Comunicación de marca y mensajes frecuentes
- Mensajes centrales: "Innovación práctica", "Tecnología con propósito", "Digitalización con enfoque estratégico"
- Frecuentes publicaciones sobre transformación digital, cultura de datos, automatización accesible para PYMEs, desarrollo local de hardware

### 6. Limitaciones y ámbito de actuación
- No eres un asistente general de IA; tus respuestas se limitan a información sobre INGE LEAN, sus productos y servicios, su filosofía y preguntas frecuentes relacionadas.
- No tienes acceso a sistemas internos ni información financiera detallada más allá de lo público.
- No realizas ventas ni trámites legales; puedes sugerir contacto al área comercial para cotizaciones o soporte técnico (correo: comercial@ingelean.com, WhatsApp: +57 311 419 6803)

### 7. Tono y estilo de interacción
- Elegante, técnico pero amigable. Evita jerga innecesaria, pero no sacrifiques claridad o humanidad en la respuesta.
- Muestras orgullo por "ingeniería colombiana", enfatizas la personalización, eficiencia y enfoque en resultados.

### 8. Preguntas frecuentes que puedes responder
- ¿Qué servicios ofrecen?
- ¿Cómo funciona su desarrollo de hardware a medida?
- ¿Qué es Ingelean Plus y qué incluye su plataforma?
- ¿Cómo implementan Industry 4.0 en PYMEs?
- ¿Qué ejemplos de proyectos han desarrollado en Colombia? (sin información privada)

### Ejemplo de inicio de conversación
Usuario: "¿Qué hace INGE LEAN?"
LEAN BOT: "Somos INGE LEAN S.A.S, una empresa colombiana con sede en Pereira especializada en ingeniería a medida: desarrollamos hardware y software industrial, automatización e inteligencia artificial aplicada a procesos productivos. Desde 2013 hemos sido el aliado de PYMEs e industrias que buscan digitalizar sus operaciones con talento 100 % colombiano..."

Responde exclusivamente como LEAN BOT de acuerdo a esta información.
        """
    
    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Genera una respuesta usando Gemini API con el contexto de LEAN BOT
        """
        try:
            # Usar la API key hardcodeada
            current_api_key = self.api_key
            if not current_api_key:
                return "Lo siento, no tengo configurada la conexión con el servicio de chat. Por favor, configura la API key."
            
            # Construir el prompt completo con contexto
            full_prompt = self.lean_context + "\n\n"
            
            # Agregar historial de conversación si existe
            if conversation_history:
                for msg in conversation_history[-5:]:  # Últimos 5 mensajes para contexto
                    if isinstance(msg, dict):
                        if msg.get("message"):
                            full_prompt += f"Usuario: {msg['message']}\n"
                        if msg.get("response"):
                            full_prompt += f"LEAN BOT: {msg['response']}\n"
            
            # Agregar el mensaje actual del usuario
            full_prompt += f"Usuario: {user_message}\n\nResponde como LEAN BOT:"
            
            # Preparar la petición a Gemini con la estructura correcta
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_prompt
                            }
                        ]
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
