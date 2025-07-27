#!/usr/bin/env python3
"""
Script para probar el nuevo sistema de persistencia con documentos y nombres
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_user_creation_and_persistence():
    print("🧪 Probando sistema de persistencia mejorado...")
    
    # Test 1: Usuario con cédula numérica
    print("\n1️⃣ Probando usuario con cédula: 1088239515")
    
    # Crear/obtener usuario
    response = requests.post(f"{BASE_URL}/usuarios/", 
                           json={"doc_id": "1088239515"})
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Usuario creado/obtenido: {user_data['doc_id']}")
        print(f"   Chat ID: {user_data['chat']['id']}")
        print(f"   Mensajes existentes: {len(user_data['chat']['mensajes']) if user_data['chat']['mensajes'] else 0}")
        
        # Enviar mensaje
        message_response = requests.post(f"{BASE_URL}/usuarios/1088239515/message",
                                       json={"message": "Hola, soy el usuario 1088239515"})
        
        if message_response.status_code == 200:
            print("✅ Mensaje enviado correctamente")
        else:
            print(f"❌ Error enviando mensaje: {message_response.status_code}")
    else:
        print(f"❌ Error creando usuario: {response.status_code}")
    
    # Test 2: Usuario con nombre
    print("\n2️⃣ Probando usuario con nombre: Juan Perez")
    
    response = requests.post(f"{BASE_URL}/usuarios/", 
                           json={"doc_id": "Juan Perez"})
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Usuario creado/obtenido: {user_data['doc_id']}")
        print(f"   Chat ID: {user_data['chat']['id']}")
        print(f"   Mensajes existentes: {len(user_data['chat']['mensajes']) if user_data['chat']['mensajes'] else 0}")
        
        # Enviar mensaje
        message_response = requests.post(f"{BASE_URL}/usuarios/Juan Perez/message",
                                       json={"message": "Hola, soy Juan Perez"})
        
        if message_response.status_code == 200:
            print("✅ Mensaje enviado correctamente")
        else:
            print(f"❌ Error enviando mensaje: {message_response.status_code}")
    else:
        print(f"❌ Error creando usuario: {response.status_code}")
    
    # Test 3: Verificar persistencia - volver a obtener usuario 1088239515
    print("\n3️⃣ Verificando persistencia del usuario 1088239515...")
    
    response = requests.post(f"{BASE_URL}/usuarios/", 
                           json={"doc_id": "1088239515"})
    
    if response.status_code == 200:
        user_data = response.json()
        mensajes_count = len(user_data['chat']['mensajes']) if user_data['chat']['mensajes'] else 0
        print(f"✅ Usuario recuperado con {mensajes_count} mensajes")
        
        if mensajes_count > 0:
            print("✅ ¡Persistencia funcionando correctamente!")
        else:
            print("⚠️ No se encontraron mensajes previos")
    else:
        print(f"❌ Error recuperando usuario: {response.status_code}")
    
    # Test 4: Obtener mensajes directamente
    print("\n4️⃣ Obteniendo mensajes del usuario 1088239515...")
    
    response = requests.get(f"{BASE_URL}/usuarios/1088239515/messages")
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ Mensajes obtenidos: {len(messages)}")
        for i, msg in enumerate(messages[:3]):  # Mostrar solo los primeros 3
            print(f"   {i+1}. {msg.get('message', 'N/A')[:50]}...")
    else:
        print(f"❌ Error obteniendo mensajes: {response.status_code}")

if __name__ == "__main__":
    try:
        test_user_creation_and_persistence()
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor. Asegúrate de que esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")