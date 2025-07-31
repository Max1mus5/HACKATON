# LEAN BOT - Guía de Despliegue

## 🚀 Opciones de Despliegue

### 1. Render (Recomendado)
```bash
# Comando de construcción:
pip install --no-cache-dir -r requirements.txt

# Comando de inicio:
uvicorn src.Backend.api:app --host 0.0.0.0 --port $PORT
```

### 2. Heroku
```bash
# Usar Procfile incluido
git push heroku main
```

### 3. Docker
```bash
docker build -t lean-bot .
docker run -p 8000:8000 lean-bot
```

### 4. Manual
```bash
pip install -r requirements.txt
uvicorn src.Backend.api:app --host 0.0.0.0 --port 8000
```

## 📦 Dependencias

### Principales
- FastAPI 0.104.1
- SQLAlchemy 2.0.21
- Transformers 4.35.0 (BETO)
- PyTorch 2.2.0

### Fallback
Si las dependencias de ML fallan, el sistema funcionará con análisis básico.

## 🔧 Variables de Entorno

```bash
PORT=8000                    # Puerto del servidor
TRANSFORMERS_CACHE=/tmp/cache # Cache de modelos
PYTHON_VERSION=3.11.9        # Versión de Python
```

## 🧪 Verificación

```bash
curl http://localhost:8000/
# Respuesta: {"message":"LEAN BOT API funcionando correctamente"}
```

## 📊 Endpoints Principales

- `GET /` - Health check
- `POST /usuarios/{doc_id}/message` - Chat
- `GET /analytics` - Dashboard analytics
- `GET /analytics/chat-details/{user_id}` - Detalles de usuario