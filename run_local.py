#!/usr/bin/env python3
"""
Script para ejecutar el backend localmente con imports correctos
Uso: python run_local.py
"""
import sys
import os
from pathlib import Path

# Agregar el directorio Backend al path para imports absolutos
backend_dir = Path(__file__).parent / "src" / "Backend"
sys.path.insert(0, str(backend_dir))

# Cambiar al directorio Backend
os.chdir(backend_dir)

# Importar y ejecutar uvicorn
import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando HACKATON Backend en modo desarrollo local...")
    print(f"📁 Directorio: {backend_dir}")
    print("🌐 URL: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("-" * 50)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_dir)]
    )