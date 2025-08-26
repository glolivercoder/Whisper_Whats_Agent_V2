@echo off
echo 🚀 Starting Whisper WhatsApp Agent with Coqui TTS Fix for Windows
echo ===============================================================

REM Set environment variables to fix MeCab issues on Windows
set MECAB_PATH=
set MECAB_CHARSET=utf8
set PYTHONIOENCODING=utf-8
set COQUI_TTS_NO_MECAB=1

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found, using system Python
)

REM Start the server
echo 🔄 Starting server...
python backend/main_enhanced.py

echo.
echo 🛑 Server stopped
pause