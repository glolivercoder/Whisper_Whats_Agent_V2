@echo off
REM Startup script for Whisper WhatsApp Agent with XTTS v2 fixes

echo ========================================
echo Starting Whisper WhatsApp Agent V2
echo With XTTS v2 Voice Cloning Fixes
echo ========================================

REM Set environment variables to fix MeCab issues on Windows
set MECAB_PATH=
set MECAB_CHARSET=utf8
set PYTHONIOENCODING=utf-8
set COQUI_TTS_NO_MECAB=1

echo [+] Environment variables set for Coqui TTS compatibility

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [+] Virtual environment activated
) else (
    echo [!] Virtual environment not found, using system Python
)

REM Run the application with all fixes
echo [+] Starting application...
python backend/main_enhanced.py

echo [+] Application finished
pause