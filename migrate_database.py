#!/usr/bin/env python3
"""
Script para migrar la base de datos de doc_id INTEGER a doc_id STRING
"""

import sqlite3
import os

def migrate_database():
    db_path = "/workspace/HACKATON/src/Backend/database.sqlite"
    
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
    
    print("🔄 Iniciando migración de base de datos...")
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Crear tabla temporal con doc_id como TEXT
        print("📋 Creando tabla temporal...")
        cursor.execute("""
            CREATE TABLE usuarios_temp (
                id TEXT PRIMARY KEY,
                doc_id TEXT NOT NULL UNIQUE,
                chat_id TEXT NOT NULL UNIQUE,
                FOREIGN KEY (chat_id) REFERENCES chats (id)
            )
        """)
        
        # 2. Copiar datos convirtiendo doc_id a string
        print("📋 Copiando datos...")
        cursor.execute("""
            INSERT INTO usuarios_temp (id, doc_id, chat_id)
            SELECT id, CAST(doc_id AS TEXT), chat_id
            FROM usuarios
        """)
        
        # 3. Eliminar tabla original
        print("📋 Eliminando tabla original...")
        cursor.execute("DROP TABLE usuarios")
        
        # 4. Renombrar tabla temporal
        print("📋 Renombrando tabla temporal...")
        cursor.execute("ALTER TABLE usuarios_temp RENAME TO usuarios")
        
        # 5. Verificar migración
        cursor.execute("SELECT doc_id, typeof(doc_id) FROM usuarios LIMIT 5")
        results = cursor.fetchall()
        
        print("✅ Migración completada exitosamente!")
        print("📊 Datos migrados:")
        for doc_id, tipo in results:
            print(f"  - doc_id: {doc_id} (tipo: {tipo})")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()