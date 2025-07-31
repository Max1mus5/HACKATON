# Configuración de API Key de Gemini para LEAN BOT

## ¿Por qué necesitas una API Key de Gemini?

El sistema de analíticas de LEAN BOT utiliza Google Gemini AI para:
- Análisis de sentimientos en tiempo real
- Scoring automático de conversaciones (1-10)
- Generación de estadísticas precisas para dashboard y admin

## Cómo obtener tu API Key de Gemini

1. **Visita Google AI Studio**
   - Ve a: https://aistudio.google.com/
   - Inicia sesión con tu cuenta de Google

2. **Crear API Key**
   - Haz clic en "Get API Key"
   - Selecciona "Create API Key in new project" o usa un proyecto existente
   - Copia la API key generada

3. **Configurar en LEAN BOT**
   - Abre el archivo: `public/js/config.js`
   - Reemplaza la línea:
     ```javascript
     geminiApiKey: "AIzaSyDGvGvGvGvGvGvGvGvGvGvGvGvGvGvGvGv"
     ```
   - Por tu API key real:
     ```javascript
     geminiApiKey: "TU_API_KEY_AQUI"
     ```

## Verificar que funciona

1. **Abrir el chatbot**
   - Ve a `/chatbot` en tu aplicación
   - Abre la consola del navegador (F12)

2. **Buscar confirmación**
   - Deberías ver: `✅ API key de Gemini configurada en el backend`
   - Si ves: `⚠️ API key de Gemini no encontrada`, revisa la configuración

3. **Probar scoring**
   - Envía algunos mensajes al chatbot
   - Ve al dashboard (`/dashboard`) o admin (`/admin`)
   - Los scores deberían variar según el sentimiento (no siempre 50%)

## Solución de problemas

### Problema: Scores siempre en 50%
- **Causa**: API key no configurada o inválida
- **Solución**: Verificar API key en config.js

### Problema: Error en consola "API key de Gemini no encontrada"
- **Causa**: config.js no cargado o API key vacía
- **Solución**: Verificar que config.js esté incluido en HTML

### Problema: "Error configurando API key de Gemini"
- **Causa**: Backend no disponible o API key inválida
- **Solución**: Verificar conexión al backend y validez de API key

## Estructura del flujo de scoring

```
Usuario envía mensaje → Backend recibe → Gemini analiza → Score 1-10 → Dashboard muestra
```

### Ejemplo de scoring:
- **Mensaje positivo**: "¡Excelente servicio, muy satisfecho!" → Score: 8-10
- **Mensaje neutral**: "Hola, necesito información" → Score: 5
- **Mensaje negativo**: "Estoy muy frustrado con esto" → Score: 1-4

## Seguridad

- **NO** subas tu API key al repositorio
- Considera usar variables de entorno en producción
- La API key se envía al backend solo para procesamiento interno

## Contacto

Si tienes problemas con la configuración, revisa:
1. Consola del navegador para errores
2. Logs del backend para confirmación de API key
3. Que el archivo config.js esté correctamente incluido en las páginas HTML