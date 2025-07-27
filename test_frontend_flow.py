#!/usr/bin/env python3
"""
Script para simular exactamente el flujo del frontend y verificar por qué no se guardan los mensajes
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://localhost:8000"  # URL local del backend
TEST_DOC_ID = 1234567890

def test_complete_frontend_flow():
    """Simula exactamente el flujo del frontend"""
    
    print("🧪 SIMULANDO FLUJO COMPLETO DEL FRONTEND")
    print("=" * 60)
    
    try:
        # 1. Verificar que el backend esté disponible
        print("1️⃣ Verificando disponibilidad del backend...")
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            print("✅ Backend disponible")
            print(f"   Respuesta: {health_response.json()}")
        else:
            print("❌ Backend no disponible")
            return
        
        # 2. Configurar API key de Gemini
        print("\n2️⃣ Configurando API key de Gemini...")
        gemini_config = {
            "api_key": "AIzaSyCzaQACaf-vJZPF1JFXPt6VSfGyfM1ZbZ0"
        }
        config_response = requests.post(f"{BASE_URL}/config/gemini_api_key", json=gemini_config)
        if config_response.status_code == 200:
            print("✅ API key configurada")
        else:
            print(f"⚠️ Error configurando API key: {config_response.status_code}")
        
        # 3. Inicializar usuario (como hace el frontend)
        print(f"\n3️⃣ Inicializando usuario con doc_id: {TEST_DOC_ID}...")
        user_data = {
            "doc_id": TEST_DOC_ID
        }
        
        user_response = requests.post(f"{BASE_URL}/usuarios/", json=user_data)
        if user_response.status_code == 200:
            user_info = user_response.json()
            print("✅ Usuario inicializado")
            print(f"   Usuario ID: {user_info['id']}")
            print(f"   Chat ID: {user_info['chat']['id']}")
            print(f"   Mensajes iniciales: {user_info['chat']['mensajes']}")
            print(f"   Score inicial: {user_info['chat']['score']}")
            
            chat_id = user_info['chat']['id']
        else:
            print(f"❌ Error inicializando usuario: {user_response.status_code}")
            print(f"   Respuesta: {user_response.text}")
            return
        
        # 4. Enviar mensajes como hace el frontend
        test_messages = [
            "Hola, necesito información sobre INGE LEAN",
            "¿Qué servicios ofrecen?",
            "Me interesa contactarlos"
        ]
        
        print(f"\n4️⃣ Enviando {len(test_messages)} mensajes...")
        
        for i, message_text in enumerate(test_messages, 1):
            print(f"\n--- Enviando mensaje {i}: {message_text} ---")
            
            # Enviar mensaje usando el endpoint que usa el frontend
            message_data = {
                "message": message_text
            }
            
            message_response = requests.post(
                f"{BASE_URL}/usuarios/{TEST_DOC_ID}/message", 
                json=message_data
            )
            
            if message_response.status_code == 200:
                response_data = message_response.json()
                print(f"✅ Respuesta recibida:")
                print(f"   Message: {response_data.get('message', 'N/A')}")
                print(f"   Response: {response_data.get('response', 'N/A')[:60]}...")
                print(f"   Score: {response_data.get('score', 'N/A')}")
                print(f"   Timestamp: {response_data.get('timestamp', 'N/A')}")
            else:
                print(f"❌ Error enviando mensaje: {message_response.status_code}")
                print(f"   Respuesta: {message_response.text}")
                continue
            
            # Pequeña pausa entre mensajes
            time.sleep(1)
        
        # 5. Verificar el estado final del usuario
        print(f"\n5️⃣ Verificando estado final del usuario...")
        
        final_user_response = requests.get(f"{BASE_URL}/usuarios/{TEST_DOC_ID}")
        if final_user_response.status_code == 200:
            final_user_info = final_user_response.json()
            print("✅ Estado final del usuario:")
            print(f"   Usuario ID: {final_user_info['id']}")
            print(f"   Doc ID: {final_user_info['doc_id']}")
            print(f"   Chat ID: {final_user_info['chat']['id']}")
            print(f"   Mensajes finales: {final_user_info['chat']['mensajes']}")
            print(f"   Score final: {final_user_info['chat']['score']}")
            
            # Analizar los mensajes
            mensajes = final_user_info['chat']['mensajes']
            if mensajes is None:
                print("❌ PROBLEMA: mensajes es NULL - no se están guardando")
            elif isinstance(mensajes, list):
                print(f"✅ Mensajes guardados: {len(mensajes)}")
                print(f"✅ Mensajes esperados: {len(test_messages)}")
                
                if len(mensajes) == len(test_messages):
                    print("🎉 TODOS LOS MENSAJES SE GUARDARON CORRECTAMENTE")
                    
                    # Mostrar estructura de cada mensaje
                    for j, msg in enumerate(mensajes, 1):
                        print(f"   Mensaje {j}:")
                        print(f"     - message: {msg.get('message', 'N/A')}")
                        print(f"     - response: {msg.get('response', 'N/A')[:50]}...")
                        print(f"     - score: {msg.get('score', 'N/A')}")
                        print(f"     - timestamp: {msg.get('timestamp', 'N/A')}")
                else:
                    print(f"⚠️ FALTAN MENSAJES: guardados={len(mensajes)}, esperados={len(test_messages)}")
            else:
                print(f"❌ PROBLEMA: mensajes no es una lista: {type(mensajes)}")
        else:
            print(f"❌ Error obteniendo estado final: {final_user_response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend. ¿Está ejecutándose?")
        print("   Ejecuta: cd src/Backend && python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def check_database_directly():
    """Verifica directamente la base de datos SQLite"""
    print(f"\n🔍 VERIFICACIÓN DIRECTA DE BASE DE DATOS")
    print("=" * 40)
    
    import sqlite3
    import os
    
    db_path = "src/Backend/database.sqlite"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cursor.fetchone()[0]
        print(f"👥 Total usuarios: {user_count}")
        
        # Verificar chats
        cursor.execute("SELECT COUNT(*) FROM chats")
        chat_count = cursor.fetchone()[0]
        print(f"💬 Total chats: {chat_count}")
        
        # Verificar chats con mensajes
        cursor.execute("SELECT id, mensajes, score FROM chats WHERE mensajes IS NOT NULL")
        chats_with_messages = cursor.fetchall()
        
        print(f"📨 Chats con mensajes: {len(chats_with_messages)}")
        
        for chat_id, mensajes_json, score in chats_with_messages:
            print(f"  Chat {chat_id[:8]}...:")
            print(f"    Score: {score}")
            if mensajes_json:
                try:
                    mensajes = json.loads(mensajes_json)
                    if isinstance(mensajes, list):
                        print(f"    Mensajes: {len(mensajes)}")
                        for i, msg in enumerate(mensajes, 1):
                            print(f"      {i}. {msg.get('message', 'N/A')[:30]}...")
                    else:
                        print(f"    Mensajes (tipo incorrecto): {type(mensajes)}")
                except json.JSONDecodeError:
                    print(f"    Mensajes (JSON inválido): {mensajes_json[:50]}...")
            else:
                print(f"    Mensajes: NULL")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")

if __name__ == "__main__":
    check_database_directly()
    test_complete_frontend_flow()