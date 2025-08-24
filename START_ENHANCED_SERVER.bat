@echo off
echo 🚀 Starting Enhanced WhatsApp Voice Agent V2
echo 📍 Port: 8001 (Enhanced Version)
echo ===============================================

cd /d "%~dp0backend"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo.
echo Starting Enhanced Server...
echo.

python main_enhanced.py

echo.
echo ❌ Server stopped. Press any key to exit...
pause