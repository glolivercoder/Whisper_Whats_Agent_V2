@echo off
echo 🚀 Starting WhatsApp Voice Agent V2 in Production Mode
echo ⚡ This will reduce file monitoring and database overhead
echo.

REM Set production environment variables
set PRODUCTION_MODE=true
set ENABLE_FILE_MONITORING=false
set LOG_LEVEL=error

echo ⚙️ Production Configuration:
echo    - File Monitoring: DISABLED
echo    - Log Level: ERROR
echo    - Database: Lazy Loading
echo.

REM Change to backend directory and start
cd /d "%~dp0backend"

REM Activate virtual environment if available
if exist "..\venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call "..\venv\Scripts\activate.bat"
)

echo 🎯 Starting enhanced server in production mode...
python main_enhanced.py

pause