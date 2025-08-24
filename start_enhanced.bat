@echo off
echo ==========================================
echo  WhatsApp Voice Agent V2 - Enhanced
echo  Complete System with LLM, TTS, Database
echo ==========================================
echo.

REM Set environment variables
set PYTHONPATH=%CD%
set ENVIRONMENT=development

REM Colors for better visibility
color 0A

echo [1/7] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.9+
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python found

echo.
echo [2/7] Checking virtual environment...
if not exist "venv" (
    echo 🔄 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)

echo.
echo [3/7] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

echo.
echo [4/7] Installing/updating enhanced dependencies...
echo 📦 Installing enhanced requirements...
pip install -r requirements_enhanced.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Trying with original requirements as fallback...
    pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo ❌ Failed to install any dependencies
        pause
        exit /b 1
    )
    echo ⚠️ Using basic requirements (some features may be limited)
) else (
    echo ✅ Enhanced dependencies installed
)

echo.
echo [5/7] Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "temp_audio" mkdir temp_audio
if not exist "models" mkdir models
echo ✅ Directories created

echo.
echo [6/7] Setting up configuration...
if not exist ".env" (
    if exist ".env.example" (
        echo 📋 Copying configuration template...
        copy .env.example .env >nul
        echo ⚠️ Please edit .env file to configure your API keys
    ) else (
        echo ⚠️ No .env.example found, creating basic .env
        echo # Basic configuration > .env
        echo OPENROUTER_API_KEY=your-api-key-here >> .env
        echo GEMINI_API_KEY=your-gemini-key-here >> .env
        echo DEFAULT_LLM_PROVIDER=local >> .env
        echo TTS_ENABLED=false >> .env
    )
) else (
    echo ✅ Configuration file exists
)

echo.
echo [7/7] Starting Enhanced WhatsApp Voice Agent V2...
echo.
echo 🌟 ================================
echo 🌟   ENHANCED FEATURES AVAILABLE
echo 🌟 ================================
echo 🎤 Advanced Whisper STT (WebM support)
echo 🧠 Multi-LLM Support (OpenRouter, Gemini)
echo 🔊 TTS Integration (Coqui TTS ready)
echo 💾 Database with conversation logging
echo 📱 Complete WhatsApp Business API
echo 🔌 Enhanced WebSocket communication
echo 📊 System monitoring and health checks
echo.
echo 🔗 ========== ACCESS POINTS ==========
echo 🏠 Main Interface:  http://localhost:8001
echo 📖 API Documentation: http://localhost:8001/docs
echo 🔍 Health Check: http://localhost:8001/health  
echo 📊 System Status: http://localhost:8001/api/status
echo 🧠 Available Models: http://localhost:8001/api/models
echo 🔌 WebSocket: ws://localhost:8001/ws
echo.
echo 📱 ========== MOBILE ACCESS ==========
echo For mobile testing, use your computer's IP:
echo Example: http://192.168.1.100:8001
echo Generate QR code at: http://localhost:8001/Manual.html
echo.
echo 🎯 ========== QUICK TESTS ==========
echo STT Test: POST audio to /api/stt
echo LLM Test: POST message to /api/llm  
echo Chat Test: POST to /api/chat
echo WebSocket: Connect to ws://localhost:8001/ws
echo.

cd backend
python main_enhanced.py

REM Fallback to simple version if enhanced fails
if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Enhanced version failed, trying simple version...
    python main_simple.py
)

echo.
echo 🏁 Server stopped
pause