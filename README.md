# LEAN - Chatbot de Exposición Electromagnética

Un chatbot interactivo desarrollado para proporcionar información y asistencia sobre exposición electromagnética.

## 🚀 Características

- **Interfaz moderna y minimalista** con diseño oscuro profesional
- **Reconocimiento de voz** para interacción manos libres
- **Integración con Google Gemini** para respuestas inteligentes
- **Diseño responsive** adaptado a dispositivos móviles
- **Configuración personalizable** de modelos y API keys

## 🎨 Paleta de Colores

```css
--color-dust-storm: #e4cfcd     /* Texto secundario */
--color-spicy-mix: #7d4e3f      /* Acentos cálidos */
--color-taupe: #413530          /* Bordes y elementos */
--color-crowshead: #150605      /* Fondo secundario */
--color-rangoon-green: #060504  /* Fondo principal */
--color-accent-orange: #FF6600  /* Color de acento principal */
--color-white: #ffffff          /* Texto principal */
```

## 📁 Estructura del Proyecto

```
├── public/                 # Archivos públicos del frontend
│   ├── index.html         # Página principal
│   ├── css/              
│   │   └── styles.css     # Estilos principales con paleta de colores
│   ├── js/               
│   │   ├── chatbot.js     # Lógica principal del chatbot
│   │   ├── config.js      # Configuración de API
│   │   └── voiceRecognition.js # Reconocimiento de voz
│   ├── data/             
│   │   └── data.json      # Datos de entrenamiento
│   └── img/              
│       ├── LOGO LEAN.png  # Logo principal
│       └── bot-icon.svg   # Icono del bot
├── src/                   # Código fuente de desarrollo
│   ├── js/               # Archivos JavaScript de desarrollo
│   └── data/             # Datos de desarrollo
├── .gitignore            
├── package.json          # Configuración del proyecto
└── README.md             
```

## 🛠️ Instalación y Configuración

1. **Clona el repositorio**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd HACKATON
   ```

2. **Configura tu API Key de Google Gemini**
   - Abre `public/index.html` en tu navegador
   - Haz clic en el botón de configuración (⚙️)
   - Ingresa tu API Key de Google Gemini
   - Selecciona el modelo deseado

3. **Ejecuta el proyecto**
   - Abre `public/index.html` en tu navegador web
   - O usa un servidor local para desarrollo

## 🎯 Uso

### Interacción por Texto
1. Escribe tu pregunta en el campo de entrada
2. Haz clic en "Enviar" o presiona Enter
3. El chatbot responderá con información relevante

### Interacción por Voz
1. Haz clic en el botón del micrófono (🎤)
2. Habla claramente tu pregunta
3. El sistema convertirá tu voz a texto automáticamente
4. La respuesta se mostrará en el chat

### Configuración Avanzada
- **Modelos disponibles:**
  - `gemini-1.5-flash`: Respuestas rápidas para consultas generales
  - `gemini-1.5-pro`: Respuestas más precisas para consultas complejas

## 🔧 Tecnologías Utilizadas

- **Frontend:** HTML5, CSS3 (Variables CSS), JavaScript ES6+
- **API:** Google Gemini AI
- **Reconocimiento de voz:** Web Speech API
- **Iconos:** Font Awesome
- **Tipografía:** Google Fonts (Inter)

## 🎨 Características de Diseño

- **Diseño oscuro profesional** que reduce la fatiga visual
- **Interfaz minimalista** con enfoque en la usabilidad
- **Animaciones suaves** y transiciones fluidas
- **Responsive design** para dispositivos móviles y desktop
- **Accesibilidad mejorada** con contrastes apropiados

## 🔐 Seguridad

- Las API keys se almacenan localmente en el navegador
- No se envían datos sensibles a servidores externos
- Configuración de CORS para APIs externas

## 🚧 Desarrollo

### Estructura de archivos mantenida:
- `src/` contiene el código fuente backend
- `public/` contiene los archivos del frontend
- Separación clara entre lógica y presentación

### Próximas mejoras:
- [ ] Implementar historial de conversaciones
- [ ] Añadir soporte para archivos adjuntos
- [ ] Mejorar la precisión del reconocimiento de voz
- [ ] Implementar modo de accesibilidad mejorado

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

---

**Desarrollado con ❤️ para el proyecto de exposición electromagnética**
