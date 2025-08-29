@echo off
echo 🚀 Iniciando servidor com todas as correções aplicadas...

REM Matar processos Python existentes
taskkill /f /im python.exe 2>nul

REM Aguardar um momento
timeout /t 2 /nobreak >nul

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Configurar variáveis de ambiente
set COQUI_TOS_AGREED=1
set COQUI_TTS_NO_MECAB=1
set PYTHONPATH=%CD%

REM Iniciar servidor
echo ✅ Iniciando servidor na porta 8001...
python backend/main_enhanced.py

pause
