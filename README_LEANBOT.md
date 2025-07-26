# 🤖 LEAN BOT - Documentación Completa

## Descripción General

LEAN BOT es un asistente virtual inteligente desarrollado para INGE LEAN que integra:
- **Backend en FastAPI** con endpoints RESTful
- **Gemini AI** para generación de respuestas inteligentes
- **Análisis de sentimientos** en tiempo real
- **Persistencia de conversaciones** en base de datos SQLite
- **Frontend responsivo** con interfaz de chat moderna

---

## 🏗️ Arquitectura del Sistema

### Backend (FastAPI)
```
src/Backend/
├── api.py                 # Endpoints principales
├── database.py            # Configuración de SQLAlchemy
├── models/
│   └── chat.py           # Modelos de Usuario y Chat
├── schemas/
│   └── chat_schemas.py   # Schemas de Pydantic
├── repositories/
│   └── chat_repository.py # Lógica de negocio
└── utils/
    ├── gemini_chat.py    # Servicio de Gemini Chat
    └── gemini_sentiment.py # Análisis de sentimientos
```

### Frontend (JavaScript)
```
public/js/
├── leanbot-api.js        # API cliente para LEAN BOT
├── chatbot.js           # Lógica de chat con fallback
├── voiceRecognition.js  # Reconocimiento de voz
└── config.js           # Configuración general
```

---

## 🔄 Flujo Completo del Chatbot

### 1. Inicialización
1. **Frontend** carga `leanbot-api.js`
2. **LeanBotAPI** verifica disponibilidad del backend
3. **Usuario** se crea automáticamente con ID único
4. **Chat** se inicializa en la base de datos

### 2. Procesamiento de Mensajes
```mermaid
graph TD
    A[Usuario envía mensaje] --> B[Frontend: leanbot-api.js]
    B --> C[Backend: POST /usuarios/{doc_id}/message]
    C --> D[Gemini: Genera respuesta]
    D --> E[Análisis de sentimiento]
    E --> F[Guardado en BD]
    F --> G[Respuesta al frontend]
```

### 3. Estructura de Mensajes
```json
{
  "message": "hola, ¿cómo estás?",
  "score": 8.0,
  "timestamp": "2025-07-26T10:23:00Z",
  "response": "¡Hola! Soy LEAN BOT de INGE LEAN. Estoy muy bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?"
}
```

---

## 🛠️ Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js (opcional, solo para frontend)
- Cuenta de Google Cloud con Gemini API habilitada

### 1. Instalación del Backend
```bash
# Navegar al directorio del proyecto
cd "c:\Users\JERON\OneDrive\Documents\Projects\Bootcamp IA\HACKATON"

# Instalar dependencias
pip install -r requirements.txt

# Configurar API Key (opcional, ya está configurada por defecto)
# set GEMINI_API_KEY=AIzaSyAel_ApU1CspuRaeqT0Z6jc0CblthtMlbE

# Iniciar el servidor
python start_backend.py
```

### 2. Acceso al Sistema
- **Frontend**: `http://localhost:8000/chat.html`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/`

---

## 📡 Endpoints de la API

### Endpoints Principales

#### `POST /usuarios/{doc_id}/message`
**Enviar mensaje al chatbot**
```json
Request:
{
  "message": "hola, ¿cómo te llamas?"
}

Response:
{
  "message": "hola, ¿cómo te llamas?",
  "score": 8.0,
  "timestamp": "2025-07-26T10:23:00Z",
  "response": "¡Hola! Soy LEAN BOT, el asistente virtual de INGE LEAN."
}
```

#### `GET /usuarios/{doc_id}/chat`
**Obtener historial del chat**

#### `POST /usuarios/`
**Crear nuevo usuario y chat**

#### `GET /test/gemini`
**Probar conexión con Gemini API**

### Endpoints Legacy (Compatibilidad)
- `PUT /chats/{chat_id}` - Actualizar chat (legacy)
- `GET /chats/{chat_id}/score` - Obtener score del chat
- `GET /chats/` - Obtener todos los chats

---

## 🤖 Características de LEAN BOT

### Identidad y Personalidad
- **Nombre**: LEAN BOT
- **Empresa**: INGE LEAN
- **Personalidad**: Amigable, profesional, servicial
- **Especialidad**: Consultoría técnica y metodologías ágiles

### Capacidades
✅ **Respuestas Inteligentes**: Powered by Gemini AI  
✅ **Análisis de Sentimientos**: Evaluación emocional en tiempo real  
✅ **Memoria Conversacional**: Mantiene contexto de la conversación  
✅ **Fallback Robusto**: Sistema local si API no está disponible  
✅ **Multimodal**: Soporte para texto y voz  
✅ **Persistencia**: Guarda todas las conversaciones  

### Tipos de Consultas Soportadas
- Información sobre INGE LEAN
- Consultas técnicas generales
- Preguntas sobre proyectos
- Soporte y asistencia
- Conversación casual

---

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
GEMINI_API_KEY=AIzaSyAel_ApU1CspuRaeqT0Z6jc0CblthtMlbE
DATABASE_URL=sqlite:///./chatbot.db
```

### Configuración de Gemini
```python
# En gemini_chat.py
self.model = "gemini-1.5-flash-latest"
self.temperature = 0.7
self.max_tokens = 300
```

### Base de Datos
- **Motor**: SQLite (por defecto)
- **Tablas**: `usuarios`, `chats`
- **Campos JSON**: `mensajes`, `score`

---

## 🚨 Manejo de Errores

### Frontend
- **Backend no disponible**: Usa sistema local de fallback
- **API timeout**: Respuesta por defecto con retry
- **Error de red**: Mensaje de conectividad

### Backend
- **Gemini API falla**: Score neutro (5.0) por defecto
- **BD no disponible**: Error HTTP 500 con mensaje descriptivo
- **Validación**: Errores HTTP 400 con detalles

---

## 📊 Monitoreo y Análisis

### Métricas Disponibles
- Score de sentimiento promedio por usuario
- Número de mensajes por conversación
- Tiempo de respuesta de la API
- Disponibilidad del servicio

### Logs
```bash
# Ver logs del backend
tail -f backend.log

# Logs en navegador
console.log("Estado LEAN BOT:", leanBotAPI.isBackendAvailable)
```

---

## 🔄 Desarrollo y Testing

### Testing del Backend
```bash
# Probar endpoint de salud
curl http://localhost:8000/

# Probar Gemini
curl http://localhost:8000/test/gemini

# Enviar mensaje de prueba
curl -X POST "http://localhost:8000/usuarios/123/message" \
     -H "Content-Type: application/json" \
     -d '{"message": "hola"}'
```

### Testing del Frontend
```javascript
// En consola del navegador
leanBotInfo(); // Ver estado del sistema
await leanBotAPI.testGeminiConnection(); // Probar Gemini
await leanBotAPI.sendMessage("hola"); // Enviar mensaje
```

---

## 🚀 Despliegue en Producción

### Docker (Recomendado)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/Backend ./src/Backend
EXPOSE 8000
CMD ["uvicorn", "src.Backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de Producción
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:5432/db
GEMINI_API_KEY=your_production_key
CORS_ORIGINS=https://yourdomain.com
```

---

## 📞 Soporte y Contacto

- **Documentación**: `/docs` endpoint
- **Issues**: Revisar logs del backend y frontend
- **Performance**: Monitorear `/test/gemini` endpoint

---

## 🔄 Roadmap

### Próximas Características
- [ ] Autenticación JWT
- [ ] Rate limiting
- [ ] Métricas avanzadas
- [ ] Soporte multiidioma
- [ ] Integración con WhatsApp
- [ ] Dashboard de administración avanzado

---

*LEAN BOT v2.0 - Desarrollado para INGE LEAN*  
*Documentación actualizada: 26 de Julio, 2025*
