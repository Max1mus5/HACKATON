# Scripts de Backend - LEAN BOT

## 🚀 Scripts Disponibles

### Windows

#### `build-backend.bat`
Instala todas las dependencias necesarias para el backend:
- Dependencias del backend (`src/Backend/requirements.txt`)
- Dependencias generales del proyecto (`requirements.txt`)

**Uso:**
```bash
.\build-backend.bat
```

#### `start-backend.bat`  
Inicia el servidor backend de LEAN BOT:
- Puerto: 8000
- Host: 0.0.0.0 (accesible desde cualquier IP)
- Modo: desarrollo con recarga automática

**Uso:**
```bash
.\start-backend.bat
```

### Linux/Mac

#### `build-backend.sh`
Versión para Unix del script de construcción.

**Uso:**
```bash
chmod +x build-backend.sh
./build-backend.sh
```

#### `start-backend.sh`
Versión para Unix del script de inicio.

**Uso:**
```bash
chmod +x start-backend.sh
./start-backend.sh
```

## 📋 Requisitos Previos

1. **Python 3.9 o superior** instalado
2. **pip** instalado y actualizado
3. **uvicorn** se instalará automáticamente con las dependencias

## 🔧 Configuración Inicial

1. Ejecutar el script de build:
   ```bash
   # Windows
   .\build-backend.bat
   
   # Linux/Mac
   ./build-backend.sh
   ```

2. Iniciar el backend:
   ```bash
   # Windows
   .\start-backend.bat
   
   # Linux/Mac
   ./start-backend.sh
   ```

3. El backend estará disponible en:
   - **API Base**: http://localhost:8000
   - **Documentación**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/

## 🛠️ URLs del Backend

### Endpoints Principales
- `GET /` - Health check
- `POST /usuarios/` - Crear usuario y chat
- `POST /usuarios/{doc_id}/message` - Enviar mensaje
- `GET /usuarios/{doc_id}/messages` - Obtener mensajes
- `POST /config/gemini_api_key` - Configurar API key

### Documentación
- `GET /docs` - Swagger UI (interfaz interactiva)
- `GET /redoc` - ReDoc (documentación alternativa)

## 🔍 Verificación

Para verificar que el backend funciona correctamente:

1. Abrir http://localhost:8000 en el navegador
2. Debe mostrar: `{"message": "LEAN BOT API funcionando correctamente", "cors": "enabled", "version": "2.0"}`

## 🐛 Solución de Problemas

### Error: "uvicorn no encontrado"
```bash
pip install uvicorn
```

### Error: "No module named 'fastapi'"
```bash
pip install fastapi
```

### Puerto 8000 ocupado
Cambiar el puerto en el script:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## 📁 Estructura del Backend

```
src/Backend/
├── main.py              # Punto de entrada de la aplicación
├── api.py               # Definición de endpoints
├── database.py          # Configuración de base de datos
├── requirements.txt     # Dependencias específicas del backend
├── models/             # Modelos de datos SQLAlchemy
├── schemas/            # Esquemas Pydantic
├── repositories/       # Lógica de acceso a datos
└── utils/              # Utilidades (Gemini, sentimientos, etc.)
```
