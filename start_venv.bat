@echo off
echo 🤖 WhatsApp Voice Agent V2 - Startup with Virtual Environment
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.8+ primeiro.
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual encontrado
)

REM Activate virtual environment
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ Arquivo requirements.txt não encontrado
    echo    Execute este script a partir da pasta raiz do projeto
    pause
    exit /b 1
)

REM Install/update dependencies
echo 📚 Verificando dependências...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ⚠️ Alguns problemas na instalação, mas continuando...
)

echo ✅ Dependências verificadas

REM Create necessary directories
if not exist "static" mkdir static
if not exist "logs" mkdir logs
if not exist "backend\temp_audio" mkdir backend\temp_audio

REM Get local IP address
echo 🌐 Detectando IP local...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4" ^| findstr /v "127.0.0.1"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)
:found_ip
set LOCAL_IP=%LOCAL_IP: =%
if not defined LOCAL_IP set LOCAL_IP=localhost

echo.
echo 🚀 Iniciando servidor...
echo ================================================================
echo 📍 Local:     http://localhost:8001
echo 📱 Rede:      http://%LOCAL_IP%:8001
echo 📖 Docs:      http://localhost:8001/docs
echo 🔍 Health:    http://localhost:8001/health
echo 📋 Manual:    Manual.html
echo ================================================================
echo.
echo 💡 Dicas importantes:
echo    • Aguarde "Whisper model loaded successfully"
echo    • Para celular: use a mesma WiFi e acesse Manual.html
echo    • Permita acesso ao microfone no navegador
echo    • Para parar: Ctrl+C
echo.

REM Start the server
cd backend
python main_simple.py