#!/bin/bash

# Script de inicio para LEAN BOT API
echo "🚀 Iniciando LEAN BOT API..."

# Instalar dependencias si no están instaladas
echo "📦 Verificando dependencias..."
pip install --no-cache-dir -r requirements.txt

# Verificar que las dependencias críticas estén instaladas
python -c "
try:
    import fastapi
    import uvicorn
    import sqlalchemy
    print('✅ Dependencias básicas OK')
except ImportError as e:
    print(f'❌ Error en dependencias básicas: {e}')
    exit(1)

try:
    import transformers
    import torch
    print('✅ Dependencias de ML OK')
except ImportError as e:
    print(f'⚠️ Dependencias de ML no disponibles: {e}')
    print('   El sistema funcionará con análisis básico')
"

# Crear directorio de logs si no existe
mkdir -p logs

# Iniciar el servidor
echo "🌟 Iniciando servidor en puerto 8000..."
exec uvicorn src.Backend.api:app --host 0.0.0.0 --port 8000 --log-level info