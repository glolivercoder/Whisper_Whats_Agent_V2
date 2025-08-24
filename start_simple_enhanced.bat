@echo off
title WhatsApp Voice Agent V2 - Simple Start
color 0A

echo ======================================
echo   🚀 WhatsApp Voice Agent V2 Enhanced
echo   📍 Simple Startup Script
echo ======================================
echo.

cd /d "%~dp0"

echo 🔧 Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ❌ Virtual environment not found. Please run: python -m venv venv
    pause
    exit /b 1
)

echo.
echo 🛑 Stopping any existing Python processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1
echo ✅ Cleanup completed

echo.
echo 🚀 Starting Enhanced Server...
echo 📍 URL: http://localhost:8001
echo 📖 Docs: http://localhost:8001/docs
echo.

cd backend
python main_enhanced.py

echo.
pause