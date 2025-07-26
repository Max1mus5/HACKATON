@echo off
echo ==============================================
echo    LEAN BOT - BUILD BACKEND
echo ==============================================

echo.
echo 📦 Instalando dependencias del backend...
cd src\Backend
pip install -r requirements.txt

echo.
echo 📦 Instalando dependencias generales del proyecto...
cd ..\..
pip install -r requirements.txt

echo.
echo ✅ Build del backend completado!
echo.
echo Para iniciar el backend, ejecuta: start-backend.bat
pause
