# Flujo de Mensajes LEAN BOT - Documentación Completa

## 📋 Resumen del Flujo

El sistema LEAN BOT ahora implementa un flujo completo de mensajes que:

1. **APPEND**: Agrega mensajes al historial existente (no sobrescribe)
2. **ANÁLISIS DE SENTIMIENTO**: Analiza cada mensaje del usuario
3. **GUARDADO COMPLETO**: Guarda mensaje, respuesta, score y timestamp
4. **ESTRUCTURA CONSISTENTE**: Mantiene el formato especificado

## 🏗️ Estructura de Mensajes

Cada mensaje se guarda con la siguiente estructura:

```json
{
  "message": "hola como te llamas",
  "score": 8.0,
  "timestamp": "2025-07-26T10:23:00Z",
  "response": "hola, muy bien y tú"
}
```

## 🔄 Flujo Completo Frontend → Backend

### 1. **Frontend (chatbot.js)**
- Usuario escribe mensaje
- Se llama a `getBotResponse(userInput)`
- Utiliza `window.leanBotAPI.sendMessage(userInput)`

### 2. **API Layer (leanbot-api.js)**
- Envía POST a `/usuarios/{doc_id}/message`
- Recibe respuesta completa con metadatos

### 3. **Backend API (api.py)**
- Endpoint: `POST /usuarios/{doc_id}/message`
- Llama a `process_message()` del repositorio

### 4. **Repository (chat_repository.py)**
- `process_message()` ejecuta:
  - Obtiene historial actual
  - Genera respuesta con Gemini
  - Analiza sentimiento
  - **HACE APPEND** del nuevo mensaje
  - Guarda en base de datos

### 5. **Base de Datos (SQLite)**
- Campo `mensajes` como JSON array
- Cada nuevo mensaje se agrega al array existente

## 🛠️ Cambios Implementados

### Backend

#### `chat_repository.py`
- ✅ Función `process_message()` corregida para hacer APPEND correcto
- ✅ Agregadas funciones `get_chat_messages()` y `get_chat_messages_by_user()`
- ✅ Manejo correcto de SQLAlchemy para campos JSON

#### `api.py`
- ✅ Nuevos endpoints para obtener solo mensajes:
  - `GET /usuarios/{doc_id}/messages`
  - `GET /chats/{chat_id}/messages`

#### `gemini_chat.py`
- ✅ Soporte para API key dinámica (no hardcodeada)
- ✅ Manejo de historial de conversación

#### `gemini_sentiment.py`
- ✅ Fallback a sentimiento neutral si no hay API key

### Frontend

#### `leanbot-api.js`
- ✅ `getChatHistory()` usa nuevo endpoint de mensajes
- ✅ Logging mejorado para debugging

#### `chatbot.js`
- ✅ `loadChatHistory()` maneja nueva estructura de mensajes
- ✅ Validación de estructura de mensajes en el historial

## 🧪 Pruebas

### Script de Prueba
Se incluye `test_flujo_completo.py` que:
- Crea usuario de prueba
- Envía varios mensajes
- Verifica que se guarden correctamente
- Valida la estructura de cada mensaje

### Ejecutar Pruebas
```bash
# Ejecutar prueba completa
python test_flujo_completo.py

# Limpiar datos de prueba
python test_flujo_completo.py --clean
```

## 📡 Endpoints de la API

### Mensajes
- `POST /usuarios/{doc_id}/message` - Enviar mensaje
- `GET /usuarios/{doc_id}/messages` - Obtener mensajes del usuario
- `GET /chats/{chat_id}/messages` - Obtener mensajes del chat

### Configuración
- `POST /config/gemini_api_key` - Configurar API key de Gemini

### Gestión de Chats
- `POST /usuarios/` - Crear usuario y chat
- `GET /usuarios/{doc_id}/chat` - Obtener chat completo
- `GET /chats/{chat_id}/score` - Obtener score del chat

## 🔧 Configuración Requerida

### Backend
1. Instalar dependencias: `pip install -r requirements.txt`
2. Configurar API key de Gemini via endpoint o variable de entorno
3. Ejecutar: `uvicorn src.Backend.main:app --reload`

### Frontend
1. Configurar API key en la interfaz de configuración
2. El sistema detecta automáticamente si el backend está disponible
3. Fallback automático al sistema local si el backend no responde

## ✅ Verificación del Flujo

Para verificar que todo funciona:

1. **Backend activo**: Verificar que la API responda en `/`
2. **Usuario creado**: El primer mensaje crea automáticamente el usuario
3. **Mensajes guardados**: Verificar en la base de datos o via API
4. **Historial cargado**: Al recargar la página, debe mostrar mensajes anteriores

## 🐛 Debugging

### Logs en Consola
- `✅ Backend LEAN BOT disponible` - Backend conectado
- `📋 Historial cargado: X conversaciones` - Historial cargado correctamente
- `🤖 Usando LEAN BOT backend para respuesta` - Usando backend para respuesta

### Verificar Base de Datos
```python
# En Python REPL
from src.Backend.database import Session
from src.Backend.repositories.chat_repository import get_all_chats_with_score

db = Session()
chats = get_all_chats_with_score(db)
print(chats)
```

## 🎯 Resultado Esperado

Después de implementar todos los cambios:

1. ✅ Los mensajes se agregan (APPEND) al historial, no se sobrescriben
2. ✅ Cada mensaje tiene la estructura exacta especificada
3. ✅ El análisis de sentimiento funciona automáticamente
4. ✅ El historial se carga correctamente al iniciar la aplicación
5. ✅ Todo se guarda persistentemente en la base de datos
6. ✅ El flujo frontend → backend → database es completamente funcional
