#!/usr/bin/env python3
"""
Script de prueba para validar el flujo completo de mensajes en LEAN BOT
Simula el envío de mensajes y verifica que se guarden correctamente en la base de datos
"""

import sys
import os
import json
from datetime import datetime

# Agregar el directorio src al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'Backend'))

from database import engine, Session as DBSession, Base
from repositories.chat_repository import create_usuario_y_chat, get_usuario_y_chat, process_message, get_chat_messages_by_user
from schemas.chat_schemas import MessageRequest

def test_flujo_completo():
    """
    Prueba el flujo completo de mensajes:
    1. Crear usuario y chat
    2. Enviar mensaje
    3. Verificar que se guarde correctamente
    4. Verificar estructura de mensajes
    """
    print("🧪 Iniciando prueba del flujo completo de LEAN BOT...")
    
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión de base de datos
    db = DBSession()
    
    try:
        # Paso 1: Crear usuario de prueba
        doc_id_prueba = 99999  # ID de prueba
        print(f"📝 Paso 1: Creando usuario con doc_id {doc_id_prueba}")
        
        # Verificar si el usuario ya existe, si no, crearlo
        usuario = get_usuario_y_chat(db, doc_id_prueba)
        if not usuario:
            usuario = create_usuario_y_chat(db, doc_id_prueba)
            print(f"✅ Usuario creado: {usuario.doc_id}, Chat ID: {usuario.chat.id}")
        else:
            print(f"✅ Usuario existente: {usuario.doc_id}, Chat ID: {usuario.chat.id}")
        
        # Paso 2: Enviar mensajes de prueba
        mensajes_prueba = [
            "Hola, ¿cómo estás?",
            "¿Qué servicios ofrece INGE LEAN?",
            "Gracias por la información"
        ]
        
        print("\n📤 Paso 2: Enviando mensajes de prueba...")
        for i, mensaje in enumerate(mensajes_prueba, 1):
            print(f"  Enviando mensaje {i}: '{mensaje}'")
            
            # Crear request de mensaje
            message_request = MessageRequest(message=mensaje, doc_id=doc_id_prueba)
            
            # Procesar mensaje completo
            response = process_message(db, usuario.chat.id, message_request)
            
            print(f"  ✅ Respuesta recibida: '{response.response[:50]}...'")
            print(f"  📊 Score de sentimiento: {response.score}")
            print(f"  🕒 Timestamp: {response.timestamp}")
        
        # Paso 3: Verificar mensajes guardados
        print("\n📋 Paso 3: Verificando mensajes guardados...")
        mensajes_guardados = get_chat_messages_by_user(db, doc_id_prueba)
        
        print(f"✅ Total de mensajes guardados: {len(mensajes_guardados)}")
        
        # Verificar estructura de cada mensaje
        for i, msg in enumerate(mensajes_guardados, 1):
            print(f"\n  📝 Mensaje {i}:")
            print(f"    - message: {msg.get('message', 'N/A')}")
            print(f"    - response: {msg.get('response', 'N/A')[:50]}...")
            print(f"    - score: {msg.get('score', 'N/A')}")
            print(f"    - timestamp: {msg.get('timestamp', 'N/A')}")
            
            # Verificar que tiene la estructura correcta
            campos_requeridos = ['message', 'response', 'score', 'timestamp']
            campos_faltantes = [campo for campo in campos_requeridos if campo not in msg]
            
            if campos_faltantes:
                print(f"    ❌ Campos faltantes: {campos_faltantes}")
            else:
                print(f"    ✅ Estructura correcta")
        
        # Paso 4: Mostrar resumen
        print(f"\n📊 Resumen de la prueba:")
        print(f"  - Usuario doc_id: {doc_id_prueba}")
        print(f"  - Chat ID: {usuario.chat.id}")
        print(f"  - Mensajes enviados: {len(mensajes_prueba)}")
        print(f"  - Mensajes guardados: {len(mensajes_guardados)}")
        print(f"  - Estado: {'✅ ÉXITO' if len(mensajes_guardados) == len(mensajes_prueba) else '❌ ERROR'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

def limpiar_datos_prueba():
    """
    Limpia los datos de prueba de la base de datos
    """
    print("\n🧹 Limpiando datos de prueba...")
    db = DBSession()
    
    try:
        doc_id_prueba = 99999
        usuario = get_usuario_y_chat(db, doc_id_prueba)
        
        if usuario:
            # Eliminar usuario y chat asociado
            db.delete(usuario.chat)
            db.delete(usuario)
            db.commit()
            print("✅ Datos de prueba eliminados")
        else:
            print("ℹ️ No hay datos de prueba para eliminar")
            
    except Exception as e:
        print(f"❌ Error al limpiar datos: {e}")
        
    finally:
        db.close()

if __name__ == "__main__":
    # Verificar si se quiere limpiar datos
    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        limpiar_datos_prueba()
    else:
        # Ejecutar prueba completa
        success = test_flujo_completo()
        
        if success:
            print("\n🎉 ¡Prueba del flujo completo exitosa!")
            print("\nPara limpiar los datos de prueba, ejecuta:")
            print("python test_flujo_completo.py --clean")
        else:
            print("\n💥 Prueba fallida. Revisa los errores arriba.")
            sys.exit(1)
