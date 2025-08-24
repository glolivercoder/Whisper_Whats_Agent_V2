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

:: Check port 8001
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001" 2^>nul') do (
    echo ⚠️  Found process using port 8001 (PID: %%a) - Terminating...
    taskkill /f /pid %%a >nul 2>&1
    if not errorlevel 1 echo ✅ Process %%a terminated successfully
)

:: Check port 8002
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8002" 2^>nul') do (
    echo ⚠️  Found process using port 8002 (PID: %%a) - Terminating...
    taskkill /f /pid %%a >nul 2>&1
    if not errorlevel 1 echo ✅ Process %%a terminated successfully
)

:: Additional cleanup - Kill any Python processes that might be running servers
echo 🧹 Cleaning up any remaining Python server processes...
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo csv 2^>nul ^| find "python.exe"') do (
    for /f "tokens=1" %%b in ('netstat -ano ^| findstr ":800" ^| findstr %%a 2^>nul') do (
        echo ⚠️  Terminating Python process %%a using port 800x...
        taskkill /f /pid %%a >nul 2>&1
    )
)

:: Wait a moment for processes to fully terminate
echo ⏳ Waiting for processes to terminate...
timeout /t 2 /nobreak >nul

:: Verify ports are free
echo 🔍 Verifying ports are free...
netstat -ano | findstr ":8001" >nul 2>&1
if not errorlevel 1 (
    echo ❌ Port 8001 still in use! Forcing cleanup...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001"') do taskkill /f /pid %%a >nul 2>&1
)

netstat -ano | findstr ":8002" >nul 2>&1
if not errorlevel 1 (
    echo ❌ Port 8002 still in use! Forcing cleanup...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8002"') do taskkill /f /pid %%a >nul 2>&1
)

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