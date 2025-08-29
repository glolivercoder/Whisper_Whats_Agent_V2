@echo off
title WhatsApp Voice Agent V2 - AMBIENTE VIRTUAL CORRIGIDO
color 0A

echo ========================================
echo  🚀 WhatsApp Voice Agent V2 Enhanced
echo  🔧 USANDO AMBIENTE VIRTUAL CORRIGIDO
echo  📍 Starting Server on Port 8001
echo ========================================
echo.

:: Navigate to project directory
cd /d "%~dp0"

:: FORÇAR uso do ambiente virtual
echo 🔄 ATIVANDO AMBIENTE VIRTUAL OBRIGATÓRIO...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Ambiente virtual ativado
) else (
    echo ❌ Ambiente virtual não encontrado!
    echo 💡 Execute: python -m venv venv
    echo 💡 Depois: venv\Scripts\activate.bat
    echo 💡 E: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo 🔍 VERIFICANDO AMBIENTE ATUAL...
python -c "import sys; print('Python path:', sys.executable)"
python -c "import sys; print('Virtual env:', 'venv' in sys.executable.lower())"

echo.
echo 🧪 TESTANDO DEPENDÊNCIAS CRÍTICAS...
python -c "
import os
os.environ['COQUI_TOS_AGREED'] = '1'
os.environ['COQUI_TTS_NO_MECAB'] = '1'
os.environ['PYTHONWARNINGS'] = 'ignore'

try:
    from TTS.api import TTS
    print('✅ TTS importado com sucesso')
    
    tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
    print('✅ XTTS v2 carregado com sucesso')
    
    print('🎉 DEPENDÊNCIAS OK - SERVIDOR PODE INICIAR')
except Exception as e:
    print(f'❌ ERRO NAS DEPENDÊNCIAS: {e}')
    print('💡 Execute fix_versions.bat primeiro')
    exit(1)
"

if errorlevel 1 (
    echo.
    echo ❌ DEPENDÊNCIAS COM PROBLEMA!
    echo 💡 Execute: fix_versions.bat
    echo 💡 Ou: remove_mecab_final.bat
    pause
    exit /b 1
)

echo.
echo 🛑 LIMPANDO PORTAS...
taskkill /f /im python.exe >nul 2>&1
for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":8001 "') do taskkill /f /pid %%i >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo 🚀 INICIANDO SERVIDOR NO AMBIENTE VIRTUAL...
echo ========================================
echo 📍 URL: http://localhost:8001
echo 🎭 Clonagem de voz: XTTS v2 ativo
echo 🔧 MeCab: Desabilitado
echo ========================================
echo.

:: CONFIGURAR AMBIENTE ANTES DE INICIAR
set COQUI_TOS_AGREED=1
set COQUI_TTS_NO_MECAB=1
set PYTHONWARNINGS=ignore

:: Navegar para backend e iniciar
cd backend
python main_enhanced.py

echo.
echo 🛑 Servidor parado. Pressione qualquer tecla...
pause