#!/usr/bin/env python3
"""
Script para probar el sistema completo de chat y verificar que el historial se guarde
"""

import os
import sys
import json
from datetime import datetime

# Configurar la API key
os.environ["GEMINI_API_KEY"] = "AIzaSyCzaQACaf-vJZPF1JFXPt6VSfGyfM1ZbZ0"

# Cambiar al directorio del backend
os.chdir('src/Backend')
sys.path.insert(0, os.getcwd())

try:
    from database import Session, engine
    from models.chat import Chat, Usuario, Base
    from repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat, process_message
    from schemas.chat_schemas import MessageRequest
    
    def test_complete_chat_flow():
        """Prueba el flujo completo de chat con múltiples mensajes"""
        
        print("🧪 TESTING COMPLETE CHAT FLOW")
        print("=" * 50)
        
        # Crear sesión de base de datos
        db = Session()
        
        try:
            # 1. Crear usuario de prueba
            test_doc_id = 12345678
            print(f"👤 Creando usuario con doc_id: {test_doc_id}")
            
            # Limpiar usuario existente si existe
            existing_user = db.query(Usuario).filter(Usuario.doc_id == test_doc_id).first()
            if existing_user:
                db.delete(existing_user.chat)
                db.delete(existing_user)
                db.commit()
                print("🧹 Usuario existente eliminado")
            
            # Crear nuevo usuario y chat
            usuario = create_usuario_y_chat(db, test_doc_id)
            print(f"✅ Usuario creado: {usuario.id}")
            print(f"✅ Chat ID: {usuario.chat_id}")
            
            # 2. Enviar múltiples mensajes para crear historial
            test_messages = [
                "Hola, soy nuevo aquí",
                "¿Qué servicios ofrece INGE LEAN?",
                "Me interesa saber sobre metodología LEAN",
                "¿Pueden ayudarme con un proyecto?",
                "Gracias por toda la información"
            ]
            
            print(f"\n📨 Enviando {len(test_messages)} mensajes...")
            
            for i, message_text in enumerate(test_messages, 1):
                print(f"\n--- Enviando mensaje {i}: {message_text} ---")
                
                # Crear request de mensaje
                message_request = MessageRequest(message=message_text)
                
                # Procesar mensaje usando la función correcta
                response = process_message(db, usuario.chat_id, message_request)
                
                print(f"✅ Respuesta recibida: {response.response[:60]}...")
                print(f"✅ Score: {response.score}")
                
                # Verificar que el historial se actualizó
                chat = db.query(Chat).filter(Chat.id == usuario.chat_id).first()
                if chat and chat.mensajes:
                    print(f"✅ Mensajes en BD: {len(chat.mensajes)}")
                    print(f"✅ Último mensaje guardado: {chat.mensajes[-1]['message'][:40]}...")
                else:
                    print("❌ No se encontraron mensajes en BD")
                    
                # Pequeña pausa para simular conversación real
                import time
                time.sleep(0.5)
            
            # 3. Verificación final del historial completo
            print(f"\n🔍 VERIFICACIÓN FINAL DEL HISTORIAL")
            print("=" * 40)
            
            final_chat = db.query(Chat).filter(Chat.id == usuario.chat_id).first()
            
            if final_chat and final_chat.mensajes:
                print(f"✅ Total mensajes guardados: {len(final_chat.mensajes)}")
                print(f"✅ Mensajes esperados: {len(test_messages)}")
                
                if len(final_chat.mensajes) == len(test_messages):
                    print("🎉 HISTORIAL COMPLETO GUARDADO CORRECTAMENTE")
                else:
                    print("❌ FALTAN MENSAJES EN EL HISTORIAL")
                
                # Mostrar el historial completo
                print(f"\n📋 HISTORIAL COMPLETO:")
                for i, msg in enumerate(final_chat.mensajes, 1):
                    print(f"  {i}. Usuario: {msg.get('message', 'N/A')[:50]}...")
                    print(f"     Bot: {msg.get('response', 'N/A')[:50]}...")
                    print(f"     Score: {msg.get('score', 'N/A')}")
                    print(f"     Timestamp: {msg.get('timestamp', 'N/A')}")
                    print()
                
                # Verificar estructura de datos
                print(f"📊 VERIFICACIÓN DE ESTRUCTURA:")
                all_valid = True
                for i, msg in enumerate(final_chat.mensajes, 1):
                    required_fields = ['message', 'response', 'score', 'timestamp']
                    missing_fields = [field for field in required_fields if field not in msg]
                    if missing_fields:
                        print(f"  ❌ Mensaje {i} - Campos faltantes: {missing_fields}")
                        all_valid = False
                    else:
                        print(f"  ✅ Mensaje {i} - Estructura completa")
                
                if all_valid:
                    print("🎉 TODAS LAS ESTRUCTURAS SON VÁLIDAS")
                else:
                    print("❌ HAY PROBLEMAS EN LA ESTRUCTURA")
                
                # Verificar orden cronológico
                print(f"\n⏰ VERIFICACIÓN DE ORDEN CRONOLÓGICO:")
                timestamps = [msg.get('timestamp') for msg in final_chat.mensajes if msg.get('timestamp')]
                if len(timestamps) == len(final_chat.mensajes):
                    sorted_timestamps = sorted(timestamps)
                    if timestamps == sorted_timestamps:
                        print("✅ Mensajes en orden cronológico correcto")
                    else:
                        print("⚠️  Mensajes NO están en orden cronológico")
                        print(f"Original: {timestamps}")
                        print(f"Ordenado: {sorted_timestamps}")
                else:
                    print("⚠️  Algunos mensajes sin timestamp")
                
            else:
                print("❌ NO SE ENCONTRÓ HISTORIAL EN LA BASE DE DATOS")
            
            # 4. Prueba de persistencia (nueva sesión)
            print(f"\n🔄 VERIFICANDO PERSISTENCIA...")
            db.close()
            
            # Nueva sesión de base de datos
            db_new = Session()
            persistent_chat = db_new.query(Chat).filter(Chat.id == usuario.chat_id).first()
            
            if persistent_chat and persistent_chat.mensajes:
                print(f"✅ Historial persiste: {len(persistent_chat.mensajes)} mensajes")
                print("✅ PERSISTENCIA CONFIRMADA")
                
                # Verificar que los datos son los mismos
                if len(persistent_chat.mensajes) == len(test_messages):
                    print("✅ Todos los mensajes persistieron correctamente")
                else:
                    print("❌ Se perdieron mensajes en la persistencia")
            else:
                print("❌ HISTORIAL NO PERSISTE")
            
            db_new.close()
            
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if 'db' in locals():
                db.close()
    
    def inspect_current_database():
        """Inspecciona el estado actual de la base de datos"""
        print(f"\n🔍 ESTADO ACTUAL DE LA BASE DE DATOS")
        print("=" * 40)
        
        db = Session()
        try:
            users_count = db.query(Usuario).count()
            chats_count = db.query(Chat).count()
            
            print(f"👥 Total usuarios: {users_count}")
            print(f"💬 Total chats: {chats_count}")
            
            # Mostrar chats con mensajes
            chats_with_messages = db.query(Chat).filter(Chat.mensajes.isnot(None)).all()
            print(f"📨 Chats con mensajes: {len(chats_with_messages)}")
            
            for i, chat in enumerate(chats_with_messages[:3], 1):
                if chat.mensajes and isinstance(chat.mensajes, list):
                    print(f"  Chat {i}: {len(chat.mensajes)} mensajes")
                    if chat.mensajes:
                        last_msg = chat.mensajes[-1]
                        print(f"    Último: {last_msg.get('message', 'N/A')[:40]}...")
        
        except Exception as e:
            print(f"❌ Error inspeccionando BD: {e}")
        finally:
            db.close()

    if __name__ == "__main__":
        inspect_current_database()
        test_complete_chat_flow()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    import traceback
    traceback.print_exc()