from typing import Optional, Dict, Any
from .gemini_chat import GeminiChatService
from .mistral_chat import MistralChatService

class AIChatService:
    """
    Servicio unificado para manejar múltiples proveedores de IA (Gemini y Mistral)
    """
    
    def __init__(self):
        self.providers = {
            "gemini": GeminiChatService,
            "mistral": MistralChatService
        }
        self.default_provider = "gemini"
    
    def get_service(self, provider: str = None, api_key: str = None):
        """
        Obtiene una instancia del servicio de IA especificado
        
        Args:
            provider: "gemini" o "mistral" (por defecto "gemini")
            api_key: API key personalizada (opcional)
        
        Returns:
            Instancia del servicio de IA correspondiente
        """
        provider = provider or self.default_provider
        
        if provider not in self.providers:
            raise ValueError(f"Proveedor no soportado: {provider}. Opciones disponibles: {list(self.providers.keys())}")
        
        service_class = self.providers[provider]
        return service_class(api_key=api_key)
    
    def generate_response(self, user_message: str, conversation_history: list = None, 
                         provider: str = None, api_key: str = None) -> Dict[str, Any]:
        """
        Genera una respuesta usando el proveedor especificado
        
        Args:
            user_message: Mensaje del usuario
            conversation_history: Historial de conversación
            provider: Proveedor de IA a usar
            api_key: API key personalizada
        
        Returns:
            Dict con la respuesta y metadatos
        """
        try:
            service = self.get_service(provider, api_key)
            response = service.generate_response(user_message, conversation_history)
            
            return {
                "response": response,
                "provider": provider or self.default_provider,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "response": "Lo siento, hubo un error al procesar tu mensaje. ¿Podrías intentarlo de nuevo?",
                "provider": provider or self.default_provider,
                "success": False,
                "error": str(e)
            }
    
    def test_provider(self, provider: str, api_key: str = None) -> Dict[str, Any]:
        """
        Prueba la conexión con un proveedor específico
        
        Args:
            provider: Proveedor a probar
            api_key: API key personalizada
        
        Returns:
            Dict con el resultado de la prueba
        """
        try:
            service = self.get_service(provider, api_key)
            is_working = service.test_connection()
            
            return {
                "provider": provider,
                "working": is_working,
                "error": None
            }
        except Exception as e:
            return {
                "provider": provider,
                "working": False,
                "error": str(e)
            }
    
    def get_available_providers(self) -> list:
        """
        Retorna la lista de proveedores disponibles
        """
        return list(self.providers.keys())