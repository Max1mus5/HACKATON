@echo off
echo ==============================================
echo    LEAN BOT - INICIANDO BACKEND
echo ==============================================

echo.
echo 🚀 Iniciando servidor backend en puerto 8000...
echo.
echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

cd src\Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
