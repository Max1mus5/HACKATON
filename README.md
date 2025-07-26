# 🤖 LEAN BOT - Sistema Completo de Chatbot Inteligente

**Un asistente virtual avanzado desarrollado para INGE LEAN con integración completa de IA**

---

## 📋 Descripción General

LEAN BOT es un sistema completo de chatbot que combina:
- **Frontend interactivo** con interfaz moderna y minimalista
- **Backend robusto** con FastAPI y integración de IA
- **Gemini AI** para respuestas inteligentes y contextuales
- **Análisis de sentimientos** en tiempo real
- **Persistencia de datos** con SQLite
- **Reconocimiento de voz** para interacción manos libres

## 🏗️ Arquitectura del Sistema

### Frontend (Interfaz de Usuario)
```
public/
├── index.html              # Página principal con redirección
├── chat.html              # Interfaz principal del chat
├── login.html             # Sistema de autenticación
├── dashboard.html         # Panel de administración
├── css/
│   ├── styles.css         # Estilos principales con diseño oscuro
│   └── bootstrap.min.css  # Framework CSS
├── js/
│   ├── leanbot-api.js     # API cliente para LEAN BOT
│   ├── chatbot.js         # Lógica principal del chatbot
│   ├── config.js          # Configuración de API
│   └── voiceRecognition.js # Reconocimiento de voz
├── data/
│   └── data.json          # Base de conocimiento local
└── img/
    ├── LOGO LEAN.png      # Logo principal
    ├── Favicon.png        # Icono del navegador
    └── bot-icon.svg       # Icono del bot
```

### Backend (Servidor API)
```
src/Backend/
├── api.py                 # Endpoints principales de la API
├── database.py            # Configuración de SQLAlchemy
├── main.py               # Punto de entrada del servidor
├── models/
│   └── chat.py           # Modelos de Usuario y Chat
├── schemas/
│   └── chat_schemas.py   # Schemas de validación
├── repositories/
│   └── chat_repository.py # Lógica de negocio
└── utils/
    ├── gemini_chat.py    # Servicio de Gemini Chat
    └── gemini_sentiment.py # Análisis de sentimientos
```

---

## 🚀 Características Principales

### ✨ **Interfaz de Usuario**
- **Diseño oscuro profesional** que reduce la fatiga visual
- **Interfaz minimalista** con enfoque en la usabilidad
- **Responsive design** para dispositivos móviles y desktop
- **Animaciones suaves** y transiciones fluidas
- **Reconocimiento de voz** integrado

### 🤖 **Inteligencia Artificial**
- **LEAN BOT Identity**: Asistente virtual de INGE LEAN
- **Gemini AI Integration**: Respuestas contextuales inteligentes
- **Análisis de sentimientos**: Evaluación emocional en tiempo real
- **Memoria conversacional**: Mantiene contexto de la conversación
- **Fallback robusto**: Sistema local si API no está disponible

### 🔧 **Backend Robusto**
- **FastAPI**: Framework moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Persistencia**: Todas las conversaciones se guardan
- **CORS configurado**: Acceso desde cualquier origen
- **API RESTful**: Endpoints bien documentados

---

## 🎨 Paleta de Colores y Diseño

```css
--color-dust-storm: #e4cfcd     /* Texto secundario */
--color-spicy-mix: #7d4e3f      /* Acentos cálidos */
--color-taupe: #413530          /* Bordes y elementos */
--color-crowshead: #150605      /* Fondo secundario */
--color-rangoon-green: #060504  /* Fondo principal */
--background-dark: #060504      /* Fondo principal actualizado */
--color-accent-orange: #FF6600  /* Color de acento principal */
--color-white: #ffffff          /* Texto principal */
```

---

## � Flujo Completo del Sistema

### 1. **Inicialización**
```mermaid
graph TD
    A[Usuario accede] --> B[Frontend verifica backend]
    B --> C[Backend disponible?]
    C -->|Sí| D[Crear/obtener usuario]
    C -->|No| E[Modo fallback local]
    D --> F[Chat listo con LEAN BOT]
    E --> G[Chat con sistema local]
```

### 2. **Procesamiento de Mensajes**
```mermaid
graph TD
    A[Usuario envía mensaje] --> B[Frontend: leanbot-api.js]
    B --> C[Backend: POST /usuarios/{doc_id}/message]
    C --> D[Gemini: Genera respuesta]
    D --> E[Análisis de sentimiento]
    E --> F[Guardado en BD]
    F --> G[Respuesta al frontend]
    G --> H[Mensaje mostrado al usuario]
```

### 3. **Estructura de Mensajes**
```json
{
  "message": "Hola, ¿cómo estás?",
  "score": 8.0,
  "timestamp": "2025-07-26T10:23:00Z",
  "response": "¡Hola! Soy LEAN BOT de INGE LEAN. Estoy muy bien, gracias por preguntar."
}
```

---

## 🛠️ Instalación y Configuración

### **Requisitos Previos**
- Python 3.8+
- Cuenta de Google Cloud con Gemini API
- Navegador web moderno

### **1. Preparación del Entorno**
```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd HACKATON

# Instalar dependencias del backend
pip install -r requirements.txt
```

### **2. Configuración de API**
```bash
# La API Key ya está configurada por defecto
# GEMINI_API_KEY=AIzaSyCzaQACaf-vJZPF1JFXPt6VSfGyfM1ZbZ0
```

### **3. Iniciar el Sistema**
```bash
# Opción 1: Script automático
python start_backend.py

# Opción 2: Manual
cd src/Backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### **4. Acceso al Sistema**
- **Chat Principal**: `http://localhost:8000/chat.html`
- **Login**: `http://localhost:8000/login.html`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/`

---

## 📡 API Endpoints

### **Endpoints Principales**

#### `POST /usuarios/{doc_id}/message`
**Enviar mensaje al chatbot LEAN BOT**
```json
Request: {"message": "hola, ¿cómo te llamas?"}
Response: {
  "message": "hola, ¿cómo te llamas?",
  "score": 8.0,
  "timestamp": "2025-07-26T10:23:00Z",
  "response": "¡Hola! Soy LEAN BOT, el asistente virtual de INGE LEAN."
}
```

#### `GET /usuarios/{doc_id}/chat`
**Obtener historial completo del chat**

#### `POST /usuarios/`
**Crear nuevo usuario y chat**

#### `GET /test/gemini`
**Probar conexión con Gemini API**

### **Endpoints de Compatibilidad**
- `PUT /chats/{chat_id}` - Actualizar chat (legacy)
- `GET /chats/{chat_id}/score` - Obtener score del chat
- `GET /chats/` - Obtener todos los chats

---

## 🎯 Uso del Sistema

### **Interacción por Texto**
1. Accede a `http://localhost:8000/chat.html`
2. Escribe tu mensaje en el campo de entrada
3. Presiona Enter o haz clic en "Enviar"
4. LEAN BOT responderá con contexto de INGE LEAN

### **Interacción por Voz**
1. Haz clic en el botón del micrófono (🎤)
2. Habla claramente tu pregunta
3. El sistema convertirá automáticamente voz a texto
4. LEAN BOT procesará y responderá

### **Configuración Avanzada**
- **Modelos Gemini disponibles:**
  - `gemini-1.5-flash-latest` (por defecto)
  - `gemini-1.5-pro-latest`
- **Configuración en tiempo real** desde la interfaz
- **Pruebas de conectividad** integradas

---

## 🧪 Testing y Monitoreo

### **Suite de Pruebas Automatizadas**
```bash
# Ejecutar todas las pruebas
python test_leanbot.py

# Pruebas específicas
python test_leanbot.py http://localhost:8000
```

### **Monitoreo en Tiempo Real**
```javascript
// En consola del navegador
leanBotInfo();                              // Estado del sistema
await leanBotAPI.testGeminiConnection();    // Probar Gemini
await leanBotAPI.sendMessage("hola");       // Enviar mensaje de prueba
```

### **Logs y Debugging**
- Backend logs en consola del servidor
- Frontend logs en consola del navegador
- Endpoint `/test/gemini` para verificar conectividad

---

## 🔧 Tecnologías Utilizadas

### **Backend**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **Requests** - Cliente HTTP

### **Frontend**
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript ES6+** - Lógica de cliente
- **Web Speech API** - Reconocimiento de voz
- **Fetch API** - Comunicación con backend
- **Bootstrap** - Framework CSS

### **Servicios de IA**
- **Google Gemini AI** - Generación de respuestas
- **Análisis de sentimientos** - Evaluación emocional
- **Procesamiento de lenguaje natural** - Comprensión contextual

---

## 🚧 Roadmap y Mejoras Futuras

### **Próximas Características**
- [ ] Autenticación JWT avanzada
- [ ] Rate limiting y throttling
- [ ] Métricas y analytics detallados
- [ ] Soporte multiidioma
- [ ] Integración con WhatsApp/Telegram
- [ ] Dashboard de administración avanzado
- [ ] Modo offline extendido
- [ ] Exportación de conversaciones

### **Optimizaciones Técnicas**
- [ ] Cache de respuestas frecuentes
- [ ] Balanceador de carga
- [ ] Base de datos en la nube
- [ ] CDN para recursos estáticos
- [ ] Monitoreo de performance

---

## 🔐 Seguridad y Privacidad

- **API Keys** se almacenan de forma segura
- **CORS configurado** apropiadamente
- **Validación de entrada** en todos los endpoints
- **Rate limiting** para prevenir abuso
- **Logs auditables** para seguimiento
- **Encriptación** de datos sensibles

---

## 📄 Licencia y Contribuciones

### **Licencia**
Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

### **Contribuciones**
Las contribuciones son bienvenidas. Por favor:
1. Abre un issue para discutir cambios mayores
2. Fork el repositorio
3. Crea una rama para tu feature
4. Envía un pull request con descripción detallada

### **Soporte**
- **Documentación**: Disponible en `/docs` del backend
- **Issues**: Usar el sistema de issues de GitHub
- **Wiki**: Documentación extendida en el wiki del proyecto

---

## 🎉 Créditos

**Desarrollado para INGE LEAN**
- **Proyecto**: Sistema de Chatbot Inteligente
- **Tecnología**: LEAN BOT v2.0
- **IA**: Powered by Google Gemini
- **Fecha**: Julio 2025

---

*LEAN BOT - El futuro de la asistencia virtual empresarial* 🚀
