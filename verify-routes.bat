@echo off
echo ==============================================
echo    VERIFICACIÓN DE RUTAS - LEAN BOT
echo ==============================================

echo.
echo 🔍 Verificando rutas en Vercel...
python verify-routes.py https://7-lean-chat.vercel.app

echo.
echo 🔍 Verificando rutas en local (si está disponible)...
python verify-routes.py http://localhost:8000

echo.
echo ✅ Verificación completada!
pause
