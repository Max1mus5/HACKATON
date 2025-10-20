"""
Gestor centralizado de API Keys para Gemini con sistema de fallback automático.
Prueba múltiples claves en orden hasta encontrar una funcional.
"""

import os
import requests
from typing import Optional, List, Tuple
from datetime import datetime


class APIKeyManager:
    """
    Gestiona múltiples API keys de Gemini con fallback automático.
    """
    
    # Lista de API keys disponibles (en orden de prioridad)
    AVAILABLE_KEYS = [
        "AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0",  # Clave original del proyecto
        "AIzaSyB-cs_l3cAYwh1WfMHA_pQHibltBPSaGrk",  # Nueva clave proporcionada
    ]
    
    def __init__(self):
        self._active_key: Optional[str] = None
        self._last_test_time: Optional[datetime] = None
        self._tested_keys: List[str] = []
    
    def get_active_key(self) -> str:
        """
        Obtiene la API key activa, probando todas las disponibles si es necesario.
        
        Returns:
            str: API key funcional
        
        Raises:
            ValueError: Si ninguna API key funciona
        """
        # 1. Verificar si hay una clave en variable de entorno
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key and env_key.strip() and self._test_api_key(env_key):
            self._active_key = env_key
            print(f"✅ Usando API key desde variable de entorno: {env_key[:15]}...")
            return env_key
        
        # 2. Si ya tenemos una clave activa y funcionó recientemente, usarla
        if self._active_key and self._test_api_key(self._active_key):
            return self._active_key
        
        # 3. Probar todas las claves disponibles
        print("🔍 Probando API keys disponibles...")
        for i, key in enumerate(self.AVAILABLE_KEYS, 1):
            print(f"   Probando clave {i}/{len(self.AVAILABLE_KEYS)}: {key[:15]}...")
            if self._test_api_key(key):
                self._active_key = key
                self._last_test_time = datetime.now()
                print(f"✅ API key funcional encontrada: {key[:15]}...")
                
                # Establecer en variable de entorno para otros servicios
                os.environ["GEMINI_API_KEY"] = key
                return key
        
        # 4. Ninguna clave funcionó
        raise ValueError(
            "❌ Ninguna API key de Gemini está funcionando. "
            "Por favor, verifica las claves o contacta al administrador."
        )
    
    def _test_api_key(self, api_key: str) -> bool:
        """
        Prueba si una API key funciona realizando una petición simple.
        
        Args:
            api_key: La API key a probar
        
        Returns:
            bool: True si la clave funciona, False en caso contrario
        """
        if not api_key or not api_key.strip():
            return False
        
        try:
            # Usar el modelo especificado en el comando del usuario
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': api_key.strip()
            }
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "Test"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=10
            )
            
            # Verificar si la respuesta es exitosa
            if response.status_code == 200:
                result = response.json()
                # Verificar que tenga la estructura esperada
                if "candidates" in result and len(result["candidates"]) > 0:
                    return True
            
            # Si llegamos aquí, la clave no funcionó
            print(f"   ❌ Clave no válida: Status {response.status_code}")
            return False
            
        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout al probar la clave")
            return False
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {str(e)[:50]}")
            return False
        except Exception as e:
            print(f"   ❌ Error inesperado: {str(e)[:50]}")
            return False
    
    def test_all_keys(self) -> List[Tuple[str, bool]]:
        """
        Prueba todas las API keys disponibles y retorna los resultados.
        
        Returns:
            List[Tuple[str, bool]]: Lista de tuplas (clave, funciona)
        """
        results = []
        print("\n🧪 Probando todas las API keys disponibles...\n")
        
        for i, key in enumerate(self.AVAILABLE_KEYS, 1):
            masked_key = f"{key[:10]}...{key[-5:]}"
            print(f"Clave {i}: {masked_key}")
            works = self._test_api_key(key)
            results.append((masked_key, works))
            print(f"   {'✅ Funciona' if works else '❌ No funciona'}\n")
        
        # También probar la clave de entorno si existe
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key and env_key not in self.AVAILABLE_KEYS:
            print(f"Clave de entorno: {env_key[:10]}...{env_key[-5:]}")
            works = self._test_api_key(env_key)
            results.append((f"ENV: {env_key[:10]}...{env_key[-5:]}", works))
            print(f"   {'✅ Funciona' if works else '❌ No funciona'}\n")
        
        return results
    
    def add_custom_key(self, api_key: str) -> bool:
        """
        Agrega y prueba una API key personalizada.
        
        Args:
            api_key: La nueva API key a agregar
        
        Returns:
            bool: True si la clave funciona y fue agregada
        """
        if not api_key or not api_key.strip():
            return False
        
        api_key = api_key.strip()
        
        # Probar la clave
        if self._test_api_key(api_key):
            # Si funciona, agregarla al inicio de la lista (mayor prioridad)
            if api_key not in self.AVAILABLE_KEYS:
                self.AVAILABLE_KEYS.insert(0, api_key)
            
            self._active_key = api_key
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"✅ API key personalizada agregada y activa: {api_key[:15]}...")
            return True
        
        print(f"❌ La API key personalizada no funciona: {api_key[:15]}...")
        return False
    
    def get_model_url(self, model_name: str = "gemini-2.0-flash") -> str:
        """
        Construye la URL completa para un modelo específico.
        
        Args:
            model_name: Nombre del modelo a usar
        
        Returns:
            str: URL completa del endpoint
        """
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"


# Instancia global del gestor
_api_key_manager: Optional[APIKeyManager] = None


def get_api_key_manager() -> APIKeyManager:
    """
    Obtiene la instancia global del gestor de API keys (Singleton).
    
    Returns:
        APIKeyManager: Instancia del gestor
    """
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager


def get_working_api_key() -> str:
    """
    Función helper para obtener una API key funcional rápidamente.
    
    Returns:
        str: API key funcional
    
    Raises:
        ValueError: Si ninguna API key funciona
    """
    manager = get_api_key_manager()
    return manager.get_active_key()
