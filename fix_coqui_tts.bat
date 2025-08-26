@echo off
echo ========================================
echo Coqui TTS Windows Fixer
echo ========================================

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Setting environment variables...
set MECAB_PATH=
set MECAB_CHARSET=utf8

echo Running Coqui TTS fix script...
python fix_coqui_tts_windows.py

echo.
echo Fix process completed.
echo Please restart your application to use the fixed Coqui TTS.

pause