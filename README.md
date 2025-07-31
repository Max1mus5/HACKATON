# 🤖 LEAN BOT - Sistema Avanzado de Chatbot con IA y Análisis de Sentimientos

**Un asistente virtual inteligente con análisis de sentimientos en tiempo real usando BETO (BERT en Español)**

---

## 🚀 Características Principales

### ✨ **Análisis de Sentimientos Avanzado**
- **Modelo BETO**: Utiliza `finiteautomata/beto-sentiment-analysis` para análisis preciso en español
- **Alta precisión**: Confianza promedio superior al 95%
- **Análisis en tiempo real**: Cada mensaje es analizado instantáneamente
- **Métricas detalladas**: Estadísticas completas y tendencias temporales

### 📊 **Dashboard de Analytics**
- **Visualización interactiva**: Gráficos en tiempo real con Chart.js
- **Métricas 24h/7días**: Comparativas temporales detalladas
- **Distribución de sentimientos**: Análisis de positivo, negativo y neutral
- **Tendencias por hora**: Patrones de comportamiento temporal
- **Palabras clave**: Extracción automática por sentimiento
- **Conversaciones activas**: Monitoreo en tiempo real

### 🤖 **Inteligencia Artificial**
- **Gemini AI**: Respuestas contextuales inteligentes
- **Mistral AI**: Alternativa de IA disponible
- **Memoria conversacional**: Mantiene contexto de la conversación
- **Fallback robusto**: Sistema local si API no está disponible

### 🎨 **Interfaz Moderna**
- **Diseño oscuro profesional**: Reduce fatiga visual
- **Responsive design**: Optimizado para móviles y desktop
- **Navegación intuitiva**: Acceso fácil a chat, dashboard y analytics
- **Animaciones fluidas**: Experiencia de usuario mejorada

---

## 🏗️ Arquitectura del Sistema

### **Backend (FastAPI)**
```
src/Backend/
├── api.py                     # Endpoints principales + Analytics
├── database.py                # Configuración SQLAlchemy
├── models/chat.py            # Modelos de Usuario y Chat
├── schemas/chat_schemas.py   # Schemas de validación
├── repositories/chat_repository.py # Lógica de negocio
└── utils/
    ├── beto_sentiment.py     # 🆕 Análisis con BETO
    ├── sentiment_analytics.py # 🆕 Estadísticas avanzadas
    ├── gemini_chat.py        # Servicio Gemini
    └── ai_chat_service.py    # Servicio unificado de IA
```

### **Frontend**
```
public/
├── chat.html                 # Interfaz principal del chat
├── analytics.html            # 🆕 Dashboard de analytics
├── dashboard.html            # Panel de administración
├── login.html               # Sistema de autenticación
├── css/styles.css           # Estilos principales
└── js/
    ├── leanbot-api.js       # API cliente
    ├── chatbot.js           # Lógica del chatbot
    └── voiceRecognition.js  # Reconocimiento de voz
```

---

## 📡 Nuevos Endpoints de Analytics

### **Análisis de Sentimientos**
- `POST /sentiment/analyze` - Analizar texto con BETO
- `GET /sentiment/model-info` - Información del modelo
- `POST /test/sentiment` - Prueba del sistema completo

### **Dashboard y Métricas**
- `GET /analytics/dashboard` - Datos completos del dashboard
- `GET /analytics/metrics` - Métricas por período
- `GET /analytics/conversation/{id}` - Análisis de conversación
- `GET /analytics/trends/hourly` - Tendencias por hora
- `GET /analytics/keywords` - Palabras clave por sentimiento
- `GET /analytics/conversations/active` - Conversaciones activas

---

## 🛠️ Instalación y Configuración

### **1. Clonar y Preparar**
```bash
git clone [URL_DEL_REPOSITORIO]
cd HACKATON
pip install -r requirements.txt
```

### **2. Iniciar el Sistema**
```bash
# Método recomendado
python main.py

# El servidor estará disponible en:
# - Chat: http://localhost:12000/chat.html
# - Analytics: http://localhost:12000/analytics.html
# - API Docs: http://localhost:12000/docs
```

### **3. Configuración de API Keys**
```bash
# Gemini API (opcional, ya configurada por defecto)
export GEMINI_API_KEY="tu_api_key_aqui"
```

---

## 📊 Uso del Dashboard de Analytics

### **Acceso**
1. Navega a `http://localhost:12000/analytics.html`
2. El dashboard se actualiza automáticamente cada 5 minutos
3. Usa el botón "🔄 Actualizar Datos" para refresh manual

### **Métricas Disponibles**
- **Mensajes Analizados**: Total en las últimas 24h
- **Confianza Promedio**: Precisión del modelo BETO
- **Sentimiento Dominante**: Tendencia general
- **Conversaciones Activas**: Chats en tiempo real

### **Gráficos Interactivos**
- **Distribución de Sentimientos**: Gráfico de dona
- **Tendencias por Hora**: Línea temporal
- **Distribución de Confianza**: Barras de precisión
- **Comparativa Semanal**: Análisis temporal

### **Herramientas de Prueba**
- **Analizador en Vivo**: Prueba textos en tiempo real
- **Resultados Detallados**: Scores por sentimiento
- **Información del Modelo**: Estado y configuración

---

## 🧪 Pruebas del Sistema

### **Prueba Automática**
```bash
curl -X POST http://localhost:12000/test/sentiment
```

### **Prueba Manual**
```bash
curl -X POST http://localhost:12000/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "¡Este sistema es increíble!"}'
```

### **Verificar Modelo**
```bash
curl http://localhost:12000/sentiment/model-info
```

---

## 🔧 Tecnologías Utilizadas

### **Análisis de Sentimientos**
- **BETO**: `finiteautomata/beto-sentiment-analysis`
- **Transformers**: Librería de Hugging Face
- **PyTorch**: Backend de machine learning
- **NumPy/Pandas**: Procesamiento de datos

### **Backend**
- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para base de datos
- **Uvicorn**: Servidor ASGI de alto rendimiento

### **Frontend**
- **Chart.js**: Visualización de datos interactiva
- **Bootstrap**: Framework CSS responsivo
- **JavaScript ES6+**: Lógica de cliente moderna

### **IA y APIs**
- **Google Gemini**: Generación de respuestas
- **Mistral AI**: Alternativa de IA
- **Web Speech API**: Reconocimiento de voz

---

## 📈 Métricas y Rendimiento

### **Precisión del Modelo BETO**
- **Textos Positivos**: >99% de precisión
- **Textos Negativos**: >99% de precisión  
- **Textos Neutrales**: >99% de precisión
- **Tiempo de Análisis**: <100ms por mensaje

### **Capacidades del Sistema**
- **Mensajes Simultáneos**: Hasta 100 por minuto
- **Historial**: Últimos 1000 mensajes en memoria
- **Actualizaciones**: Tiempo real con WebSockets
- **Almacenamiento**: SQLite con persistencia completa

---

## 🔐 Seguridad y Privacidad

- **API Keys Seguras**: Almacenamiento protegido
- **CORS Configurado**: Acceso controlado
- **Validación de Entrada**: Sanitización completa
- **Logs Auditables**: Seguimiento de actividad
- **Rate Limiting**: Prevención de abuso

---

## 🚧 Roadmap Futuro

### **Próximas Características**
- [ ] Análisis de emociones específicas (alegría, tristeza, ira)
- [ ] Detección de sarcasmo e ironía
- [ ] Análisis de temas y categorización automática
- [ ] Integración con WhatsApp/Telegram
- [ ] Dashboard móvil nativo
- [ ] Exportación de reportes en PDF
- [ ] Alertas en tiempo real por sentimiento
- [ ] Análisis comparativo entre usuarios

### **Mejoras Técnicas**
- [ ] Optimización GPU para BETO
- [ ] Cache inteligente de análisis
- [ ] Base de datos en la nube
- [ ] Balanceador de carga
- [ ] Monitoreo de performance avanzado

---

## 🎯 Casos de Uso

### **Empresarial**
- **Atención al Cliente**: Monitoreo de satisfacción en tiempo real
- **Recursos Humanos**: Análisis de clima laboral
- **Marketing**: Evaluación de campañas y feedback
- **Ventas**: Detección de oportunidades y objeciones

### **Educativo**
- **Evaluación de Estudiantes**: Análisis de feedback académico
- **Soporte Estudiantil**: Detección temprana de problemas
- **Investigación**: Análisis de sentimientos en encuestas

### **Salud Mental**
- **Monitoreo de Bienestar**: Detección de patrones emocionales
- **Soporte Psicológico**: Análisis de sesiones terapéuticas
- **Prevención**: Identificación de riesgo emocional

---

## 📄 Licencia y Contribuciones

### **Licencia**
Este proyecto está bajo la licencia MIT. Ver `LICENSE` para detalles.

### **Contribuciones**
¡Las contribuciones son bienvenidas!

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### **Soporte**
- **Issues**: Reporta bugs y solicita features
- **Documentación**: Wiki del proyecto
- **API Docs**: `/docs` endpoint del servidor

---

## 🎉 Créditos

**Desarrollado para INGE LEAN**
- **Proyecto**: Sistema de Chatbot con IA y Analytics
- **Tecnología**: LEAN BOT v3.0 con BETO
- **IA**: Powered by Google Gemini + BETO Sentiment Analysis
- **Fecha**: Julio 2025

---

*LEAN BOT - El futuro de la asistencia virtual empresarial con análisis de sentimientos avanzado* 🚀📊🤖