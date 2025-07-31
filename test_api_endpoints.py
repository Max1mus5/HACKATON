#!/usr/bin/env python3
"""
Script de prueba para los nuevos endpoints de la API
"""

import requests
import json

BASE_URL = "https://hackaton-d1h6.onrender.com"

def test_providers_endpoint():
    """Probar endpoint de proveedores disponibles"""
    print("🔍 Probando endpoint /ai/providers...")
    
    try:
        response = requests.get(f"{BASE_URL}/ai/providers")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Éxito: {data}")
            return True
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def test_ai_test_endpoint():
    """Probar endpoint de prueba de IA"""
    print("\n🧪 Probando endpoint /ai/test...")
    
    # Probar Gemini
    print("   🔵 Probando Gemini...")
    try:
        response = requests.post(f"{BASE_URL}/ai/test", json={
            "provider": "gemini"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Gemini: {data}")
        else:
            print(f"      ❌ Error Gemini {response.status_code}: {response.text}")
    except Exception as e:
        print(f"      ❌ Error Gemini: {e}")
    
    # Probar Mistral
    print("   🟠 Probando Mistral...")
    try:
        response = requests.post(f"{BASE_URL}/ai/test", json={
            "provider": "mistral"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Mistral: {data}")
        else:
            print(f"      ❌ Error Mistral {response.status_code}: {response.text}")
    except Exception as e:
        print(f"      ❌ Error Mistral: {e}")

def test_message_with_mistral():
    """Probar envío de mensaje usando Mistral"""
    print("\n💬 Probando mensaje con Mistral...")
    
    # Primero crear un usuario de prueba
    user_id = "test_mistral_user"
    
    try:
        # Crear usuario
        response = requests.post(f"{BASE_URL}/usuarios", json={
            "doc_id": user_id
        })
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Usuario creado/encontrado")
        else:
            print(f"   ⚠️ Usuario: {response.status_code}")
        
        # Enviar mensaje con Mistral
        response = requests.post(f"{BASE_URL}/usuarios/{user_id}/message", json={
            "message": "¿Qué servicios ofrece INGE LEAN?",
            "ai_provider": "mistral"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Mensaje enviado con Mistral")
            print(f"   📝 Respuesta: {data.get('response', '')[:100]}...")
            print(f"   🤖 Proveedor usado: {data.get('ai_provider', 'N/A')}")
            return True
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_message_with_custom_api_key():
    """Probar mensaje con API key personalizada"""
    print("\n🔑 Probando mensaje con API key personalizada...")
    
    user_id = "test_custom_key_user"
    custom_api_key = "bfab35a9873a475085aa3176ef879f26"  # API key de Mistral
    
    try:
        # Crear usuario
        response = requests.post(f"{BASE_URL}/usuarios", json={
            "doc_id": user_id
        })
        
        # Enviar mensaje con API key personalizada
        response = requests.post(f"{BASE_URL}/usuarios/{user_id}/message", json={
            "message": "Hola, ¿cómo funciona su servicio de automatización?",
            "ai_provider": "mistral",
            "api_key": custom_api_key
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Mensaje enviado con API key personalizada")
            print(f"   📝 Respuesta: {data.get('response', '')[:100]}...")
            print(f"   🤖 Proveedor usado: {data.get('ai_provider', 'N/A')}")
            return True
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Probando nuevos endpoints de la API\n")
    
    # Probar endpoints
    providers_ok = test_providers_endpoint()
    test_ai_test_endpoint()
    mistral_message_ok = test_message_with_mistral()
    custom_key_ok = test_message_with_custom_api_key()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Endpoint /ai/providers: {'✅' if providers_ok else '❌'}")
    print(f"   Mensaje con Mistral: {'✅' if mistral_message_ok else '❌'}")
    print(f"   API key personalizada: {'✅' if custom_key_ok else '❌'}")
    print("="*50)