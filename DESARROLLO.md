# 🚀 HACKATON - Guía de Desarrollo

## 🔧 Configuración de Desarrollo Local

### Backend
```bash
# Opción 1: Script automático (RECOMENDADO)
python run_local.py

# Opción 2: Manual desde Backend/
cd src/Backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Servidor estático simple
cd public
python -m http.server 3000

# O usar Live Server en VS Code
```

## 📁 Estructura de Imports

### ⚠️ IMPORTANTE: Diferencia Desarrollo vs Producción

**DESARROLLO LOCAL:**
- Ejecutar desde: `src/Backend/`
- Imports: Relativos funcionan con script `run_local.py`

**PRODUCCIÓN (Render):**
- Ejecutar desde: raíz del proyecto
- Comando: `uvicorn src.Backend.api:app`
- Imports: Relativos (`.database`, `..models`)

## 🔑 API Keys

### Gemini API
```
Actual: AIzaSyCrzdwv-viQnqcFnc7PBAimEzyDMf4dXY0
```

### GitHub Token
```
[Configurado en variables de entorno]
```

## 🧪 Testing

### Probar API
```bash
# Test básico
curl -X POST "http://localhost:8000/usuarios/12345/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola LEAN BOT"}'

# Ver historial
curl -X GET "http://localhost:8000/usuarios/12345"
```

## 🚨 Troubleshooting

### Error: ModuleNotFoundError
- **Causa**: Imports incorrectos para el contexto
- **Solución**: Usar `run_local.py` para desarrollo

### Error: 429 Too Many Requests
- **Causa**: API key de Gemini agotada
- **Solución**: Verificar que se use la nueva key

### Error: CORS
- **Causa**: Frontend y backend en puertos diferentes
- **Solución**: CORS ya configurado en FastAPI

## 📊 URLs Importantes

- **Backend Local**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend Local**: http://localhost:3000
- **Producción**: https://hackaton-d1h6.onrender.com

## 🔄 Workflow de Desarrollo

1. **Hacer cambios** en código
2. **Probar localmente** con `run_local.py`
3. **Commit y push** a master
4. **Verificar** deploy automático en Render
5. **Probar** en producción

## ⚡ Scripts Útiles

```bash
# Iniciar desarrollo completo
python run_local.py &
cd public && python -m http.server 3000

# Ver logs en tiempo real
tail -f local_server.log

# Reiniciar backend
pkill -f uvicorn && python run_local.py
```