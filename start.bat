@echo off
echo 🚀 Iniciando WhatsApp Voice Agent V2...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📚 Instalando dependências...
pip install -r requirements.txt

REM Criar diretórios necessários
if not exist "static" mkdir static
if not exist "logs" mkdir logs

REM Obter IP da máquina
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP: =%

echo.
echo ✅ Servidor pronto!
echo 🌐 Acesse no navegador: http://localhost:8000
echo 📱 Para WhatsApp configure webhook: http://%IP%:8000/api/whatsapp/webhook
echo.

REM Iniciar servidor
echo 🚀 Iniciando servidor FastAPI...
cd backend
python main.py