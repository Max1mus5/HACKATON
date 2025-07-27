#!/usr/bin/env python3
"""
Script simple para verificar el contenido de la base de datos SQLite
"""

import sqlite3
import json
import os

def check_database():
    """Verifica el contenido de la base de datos"""
    
    db_path = "src/Backend/database.sqlite"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {db_path}")
        return
    
    print("🔍 VERIFICANDO BASE DE DATOS")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
        # Verificar estructura de tabla chats
        if ('chats',) in tables:
            cursor.execute("PRAGMA table_info(chats);")
            columns = cursor.fetchall()
            print(f"\n📊 Estructura tabla 'chats':")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM chats;")
        chat_count = cursor.fetchone()[0]
        print(f"\n💬 Total de chats: {chat_count}")
        
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        user_count = cursor.fetchone()[0]
        print(f"👥 Total de usuarios: {user_count}")
        
        # Verificar chats con mensajes
        cursor.execute("SELECT id, mensajes, score, created_at FROM chats WHERE mensajes IS NOT NULL;")
        chats_with_messages = cursor.fetchall()
        
        print(f"\n📨 Chats con mensajes: {len(chats_with_messages)}")
        
        for i, (chat_id, mensajes_json, score, created_at) in enumerate(chats_with_messages[:3], 1):
            print(f"\n  Chat {i} (ID: {chat_id[:8]}...):")
            print(f"    - Creado: {created_at}")
            print(f"    - Score: {score}")
            
            if mensajes_json:
                try:
                    mensajes = json.loads(mensajes_json)
                    if isinstance(mensajes, list):
                        print(f"    - Mensajes: {len(mensajes)}")
                        
                        # Mostrar estructura del último mensaje
                        if mensajes:
                            last_msg = mensajes[-1]
                            print(f"    - Último mensaje:")
                            print(f"      * message: {last_msg.get('message', 'N/A')[:40]}...")
                            print(f"      * response: {last_msg.get('response', 'N/A')[:40]}...")
                            print(f"      * score: {last_msg.get('score', 'N/A')}")
                            print(f"      * timestamp: {last_msg.get('timestamp', 'N/A')}")
                            
                            # Verificar que es un append correcto
                            if len(mensajes) > 1:
                                print(f"    - Historial completo:")
                                for j, msg in enumerate(mensajes, 1):
                                    print(f"      {j}. {msg.get('message', 'N/A')[:30]}...")
                    else:
                        print(f"    - Mensajes (formato incorrecto): {type(mensajes)}")
                        
                except json.JSONDecodeError as e:
                    print(f"    - Error decodificando JSON: {e}")
            else:
                print(f"    - Sin mensajes")
        
        # Verificar si hay mensajes duplicados o problemas de append
        cursor.execute("""
            SELECT id, mensajes FROM chats 
            WHERE mensajes IS NOT NULL 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        
        recent_chats = cursor.fetchall()
        print(f"\n🔄 VERIFICACIÓN DE APPEND:")
        
        for chat_id, mensajes_json in recent_chats:
            if mensajes_json:
                try:
                    mensajes = json.loads(mensajes_json)
                    if isinstance(mensajes, list) and len(mensajes) > 1:
                        print(f"  Chat {chat_id[:8]}... - {len(mensajes)} mensajes:")
                        
                        # Verificar timestamps para confirmar orden cronológico
                        timestamps = [msg.get('timestamp') for msg in mensajes if msg.get('timestamp')]
                        if len(timestamps) == len(mensajes):
                            print(f"    ✅ Todos los mensajes tienen timestamp")
                            # Verificar orden cronológico
                            sorted_timestamps = sorted(timestamps)
                            if timestamps == sorted_timestamps:
                                print(f"    ✅ Mensajes en orden cronológico correcto")
                            else:
                                print(f"    ⚠️  Mensajes NO están en orden cronológico")
                        else:
                            print(f"    ⚠️  Algunos mensajes sin timestamp")
                            
                except json.JSONDecodeError:
                    print(f"  Chat {chat_id[:8]}... - Error JSON")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")

def test_manual_insert():
    """Prueba manual de inserción para verificar el append"""
    print(f"\n🧪 PRUEBA MANUAL DE APPEND")
    print("=" * 30)
    
    db_path = "src/Backend/database.sqlite"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear un chat de prueba
        test_chat_id = "test_chat_123"
        
        # Eliminar si existe
        cursor.execute("DELETE FROM chats WHERE id = ?", (test_chat_id,))
        
        # Insertar chat inicial
        initial_messages = [
            {
                "message": "Primer mensaje",
                "response": "Primera respuesta",
                "score": 7.0,
                "timestamp": "2024-01-01T10:00:00"
            }
        ]
        
        cursor.execute("""
            INSERT INTO chats (id, mensajes, score, created_at, updated_at)
            VALUES (?, ?, ?, datetime('now'), datetime('now'))
        """, (test_chat_id, json.dumps(initial_messages), 7.0))
        
        print("✅ Chat inicial creado con 1 mensaje")
        
        # Simular append - obtener mensajes existentes
        cursor.execute("SELECT mensajes FROM chats WHERE id = ?", (test_chat_id,))
        result = cursor.fetchone()
        
        if result and result[0]:
            existing_messages = json.loads(result[0])
            print(f"✅ Mensajes existentes recuperados: {len(existing_messages)}")
            
            # Agregar nuevo mensaje (simular append)
            new_message = {
                "message": "Segundo mensaje",
                "response": "Segunda respuesta", 
                "score": 8.0,
                "timestamp": "2024-01-01T10:05:00"
            }
            
            existing_messages.append(new_message)
            
            # Actualizar en BD
            cursor.execute("""
                UPDATE chats 
                SET mensajes = ?, score = ?, updated_at = datetime('now')
                WHERE id = ?
            """, (json.dumps(existing_messages), 8.0, test_chat_id))
            
            print("✅ Segundo mensaje agregado via append")
            
            # Verificar resultado
            cursor.execute("SELECT mensajes FROM chats WHERE id = ?", (test_chat_id,))
            final_result = cursor.fetchone()
            
            if final_result and final_result[0]:
                final_messages = json.loads(final_result[0])
                print(f"✅ Verificación final: {len(final_messages)} mensajes")
                
                for i, msg in enumerate(final_messages, 1):
                    print(f"  {i}. {msg['message']} -> {msg['response']}")
                
                if len(final_messages) == 2:
                    print("✅ APPEND FUNCIONANDO CORRECTAMENTE")
                else:
                    print("❌ APPEND NO FUNCIONA")
            
        conn.commit()
        
        # Limpiar
        cursor.execute("DELETE FROM chats WHERE id = ?", (test_chat_id,))
        conn.commit()
        conn.close()
        
        print("🧹 Chat de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error en prueba manual: {e}")

if __name__ == "__main__":
    check_database()
    test_manual_insert()