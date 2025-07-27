#!/usr/bin/env python3
"""
Script de prueba para el servicio de Mistral AI
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'Backend'))

from utils.mistral_chat import MistralChatService
from utils.ai_chat_service import AIChatService

def test_mistral_direct():
    """Prueba directa del servicio de Mistral"""
    print("🧪 Probando servicio de Mistral AI directamente...")
    
    mistral_service = MistralChatService()
    
    # Probar conexión
    print("📡 Probando conexión...")
    is_working = mistral_service.test_connection()
    print(f"   Resultado: {'✅ Funcionando' if is_working else '❌ No funciona'}")
    
    if is_working:
        # Probar mensaje
        print("\n💬 Enviando mensaje de prueba...")
        response = mistral_service.generate_response("¿Qué servicios ofrece INGE LEAN?")
        print(f"   Respuesta: {response[:100]}...")
    
    return is_working

def test_unified_service():
    """Prueba del servicio unificado"""
    print("\n🔧 Probando servicio unificado de IA...")
    
    ai_service = AIChatService()
    
    # Probar proveedores disponibles
    providers = ai_service.get_available_providers()
    print(f"   Proveedores disponibles: {providers}")
    
    # Probar Mistral
    print("\n🤖 Probando Mistral a través del servicio unificado...")
    result = ai_service.generate_response(
        "Hola, ¿cómo estás?",
        provider="mistral"
    )
    
    print(f"   Éxito: {result['success']}")
    print(f"   Proveedor usado: {result['provider']}")
    print(f"   Respuesta: {result['response'][:100]}...")
    
    if not result['success']:
        print(f"   Error: {result['error']}")
    
    return result['success']

def test_both_providers():
    """Comparar respuestas de ambos proveedores"""
    print("\n⚖️ Comparando respuestas de ambos proveedores...")
    
    ai_service = AIChatService()
    question = "¿Qué hace INGE LEAN?"
    
    # Probar Gemini
    print("\n🔵 Gemini:")
    gemini_result = ai_service.generate_response(question, provider="gemini")
    print(f"   Éxito: {gemini_result['success']}")
    if gemini_result['success']:
        print(f"   Respuesta: {gemini_result['response'][:150]}...")
    else:
        print(f"   Error: {gemini_result['error']}")
    
    # Probar Mistral
    print("\n🟠 Mistral:")
    mistral_result = ai_service.generate_response(question, provider="mistral")
    print(f"   Éxito: {mistral_result['success']}")
    if mistral_result['success']:
        print(f"   Respuesta: {mistral_result['response'][:150]}...")
    else:
        print(f"   Error: {mistral_result['error']}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de Mistral AI\n")
    
    # Prueba 1: Servicio directo
    mistral_works = test_mistral_direct()
    
    # Prueba 2: Servicio unificado
    unified_works = test_unified_service()
    
    # Prueba 3: Comparación
    if mistral_works and unified_works:
        test_both_providers()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Mistral directo: {'✅' if mistral_works else '❌'}")
    print(f"   Servicio unificado: {'✅' if unified_works else '❌'}")
    print("="*50)