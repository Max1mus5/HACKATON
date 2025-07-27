#!/usr/bin/env python3
"""
Script para verificar que el historial de chat se esté guardando correctamente en la base de datos
"""

import os
import sys
import json
from datetime import datetime

# Configurar la API key
os.environ["GEMINI_API_KEY"] = "AIzaSyCzaQACaf-vJZPF1JFXPt6VSfGyfM1ZbZ0"

# Agregar el directorio del backend al path
sys.path.append('src/Backend')

try:
    # Cambiar al directorio del backend para imports correctos
    os.chdir('src/Backend')
    sys.path.insert(0, os.getcwd())
    
    from database import Session, engine
    from models.chat import Chat, Usuario, Base
    from repositories.chat_repository import process_message
    from repositories.user_repository import create_user, get_user_by_doc_id
    from pydantic import BaseModel
    
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    class MessageRequest(BaseModel):
        message: str
        
    def test_chat_history_persistence():
        """Prueba que el historial de chat se guarde correctamente"""
        
        print("🧪 TESTING CHAT HISTORY PERSISTENCE")
        print("=" * 60)
        
        # Crear sesión de base de datos
        db = Session()
        
        try:
            # 1. Crear un usuario de prueba
            test_doc_id = 99999999
            print(f"📝 Creando usuario de prueba con doc_id: {test_doc_id}")
            
            # Limpiar usuario existente si existe
            existing_user = db.query(Usuario).filter(Usuario.doc_id == test_doc_id).first()
            if existing_user:
                db.delete(existing_user.chat)
                db.delete(existing_user)
                db.commit()
                print("🧹 Usuario existente eliminado")
            
            # Crear nuevo usuario
            user = create_user(test_doc_id, db)
            print(f"✅ Usuario creado: {user.id}")
            print(f"✅ Chat asociado: {user.chat_id}")
            
            # 2. Enviar varios mensajes para crear historial
            test_messages = [
                "Hola, ¿cómo estás?",
                "¿Puedes ayudarme con información sobre LEAN?",
                "Gracias por la información",
                "¿Qué más puedes hacer?",
                "Perfecto, muy útil"
            ]
            
            print(f"\n📨 Enviando {len(test_messages)} mensajes...")
            
            for i, message_text in enumerate(test_messages, 1):
                print(f"\n--- Mensaje {i}: {message_text} ---")
                
                # Crear request
                message_request = MessageRequest(message=message_text)
                
                # Procesar mensaje
                response = process_message(message_request, test_doc_id, db)
                
                print(f"✅ Respuesta: {response['response'][:50]}...")
                print(f"✅ Score: {response['score']}")
                
                # Verificar que el chat se actualizó
                chat = db.query(Chat).filter(Chat.id == user.chat_id).first()
                if chat and chat.mensajes:
                    print(f"✅ Mensajes en BD: {len(chat.mensajes)}")
                    print(f"✅ Último mensaje: {chat.mensajes[-1]['message'][:30]}...")
                else:
                    print("❌ No se encontraron mensajes en BD")
            
            # 3. Verificar el historial completo
            print(f"\n🔍 VERIFICACIÓN FINAL DEL HISTORIAL")
            print("=" * 40)
            
            final_chat = db.query(Chat).filter(Chat.id == user.chat_id).first()
            
            if final_chat and final_chat.mensajes:
                print(f"✅ Total de mensajes guardados: {len(final_chat.mensajes)}")
                print(f"✅ Mensajes esperados: {len(test_messages)}")
                
                if len(final_chat.mensajes) == len(test_messages):
                    print("✅ HISTORIAL COMPLETO GUARDADO CORRECTAMENTE")
                else:
                    print("❌ FALTAN MENSAJES EN EL HISTORIAL")
                
                # Mostrar estructura de cada mensaje
                print(f"\n📋 ESTRUCTURA DEL HISTORIAL:")
                for i, msg in enumerate(final_chat.mensajes, 1):
                    print(f"  Mensaje {i}:")
                    print(f"    - message: {msg.get('message', 'N/A')[:40]}...")
                    print(f"    - response: {msg.get('response', 'N/A')[:40]}...")
                    print(f"    - score: {msg.get('score', 'N/A')}")
                    print(f"    - timestamp: {msg.get('timestamp', 'N/A')}")
                    
                    # Verificar que todos los campos requeridos están presentes
                    required_fields = ['message', 'response', 'score', 'timestamp']
                    missing_fields = [field for field in required_fields if field not in msg]
                    if missing_fields:
                        print(f"    ❌ Campos faltantes: {missing_fields}")
                    else:
                        print(f"    ✅ Estructura completa")
                    print()
                
            else:
                print("❌ NO SE ENCONTRÓ HISTORIAL EN LA BASE DE DATOS")
            
            # 4. Verificar persistencia (cerrar y reabrir sesión)
            print(f"\n🔄 VERIFICANDO PERSISTENCIA...")
            db.close()
            
            # Nueva sesión
            db_new = Session()
            persistent_chat = db_new.query(Chat).filter(Chat.id == user.chat_id).first()
            
            if persistent_chat and persistent_chat.mensajes:
                print(f"✅ Historial persiste después de cerrar sesión: {len(persistent_chat.mensajes)} mensajes")
                print("✅ PERSISTENCIA CONFIRMADA")
            else:
                print("❌ HISTORIAL NO PERSISTE")
            
            db_new.close()
            
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
    
    def inspect_database():
        """Inspecciona el contenido actual de la base de datos"""
        print(f"\n🔍 INSPECCIÓN DE BASE DE DATOS")
        print("=" * 40)
        
        db = Session()
        try:
            # Contar usuarios y chats
            users_count = db.query(Usuario).count()
            chats_count = db.query(Chat).count()
            
            print(f"👥 Total usuarios: {users_count}")
            print(f"💬 Total chats: {chats_count}")
            
            # Mostrar algunos chats con mensajes
            chats_with_messages = db.query(Chat).filter(Chat.mensajes.isnot(None)).all()
            print(f"📨 Chats con mensajes: {len(chats_with_messages)}")
            
            for i, chat in enumerate(chats_with_messages[:3], 1):  # Mostrar solo los primeros 3
                if chat.mensajes:
                    print(f"\n  Chat {i} (ID: {chat.id[:8]}...):")
                    print(f"    - Mensajes: {len(chat.mensajes)}")
                    print(f"    - Creado: {chat.created_at}")
                    print(f"    - Actualizado: {chat.updated_at}")
                    if chat.mensajes:
                        print(f"    - Último mensaje: {chat.mensajes[-1].get('message', 'N/A')[:40]}...")
        
        except Exception as e:
            print(f"❌ Error inspeccionando BD: {e}")
        finally:
            db.close()

    if __name__ == "__main__":
        inspect_database()
        test_chat_history_persistence()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Instalando dependencias necesarias...")
    os.system("pip install sqlalchemy pydantic")