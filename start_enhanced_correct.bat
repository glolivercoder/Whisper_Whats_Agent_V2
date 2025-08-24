@echo off
title WhatsApp Voice Agent V2 Enhanced - Startup
color 0A

echo ========================================
echo  🚀 WhatsApp Voice Agent V2 Enhanced
echo  📍 Starting Correct Server on Port 8001
echo ========================================
echo.

:: Navigate to project directory
cd /d "%~dp0"

:: Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    echo 🔄 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found
    echo 🔄 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo 🔄 Activating virtual environment...
    call venv\Scripts\activate.bat
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo 🔄 Checking Python and dependencies...
python --version
echo.

:: Stop any existing servers on ports 8001/8002
echo 🛑 Checking and stopping any existing servers...
echo.

:: Simple port cleanup using taskkill
echo 🧹 Cleaning up ports 8001 and 8002...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1

:: Kill processes by port (Windows 10/11 method)
for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":8001 "') do taskkill /f /pid %%i >nul 2>&1
for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":8002 "') do taskkill /f /pid %%i >nul 2>&1

:: Wait a moment for processes to fully terminate
echo ⏳ Waiting for processes to terminate...
timeout /t 3 /nobreak >nul

echo ✅ Port cleanup completed

echo.
echo 🚀 Starting Enhanced Server on Port 8001...
echo 📍 URL: http://localhost:8001
echo 📖 API Docs: http://localhost:8001/docs
echo 🔍 Health: http://localhost:8001/health
echo.
echo ⚠️  IMPORTANT: Make sure to access http://localhost:8001 (NOT 8002)
echo.

:: Navigate to backend and start enhanced server
cd backend
python main_enhanced.py

echo.
echo 🛑 Server stopped. Press any key to exit...
pause