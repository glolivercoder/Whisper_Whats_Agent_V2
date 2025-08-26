@echo off
cls
echo ========================================
echo WhatsApp Voice Agent V2 - Enhanced
echo With Coqui TTS Windows Fix
echo ========================================
echo.

echo 🧹 Cleaning up ports...
call cleanup_ports.bat

echo.
echo 🔧 Applying Coqui TTS environment fixes...
set MECAB_PATH=
set MECAB_CHARSET=utf8
set PYTHONIOENCODING=utf-8

echo ✅ Environment variables set

echo.
echo 🚀 Starting Enhanced Server...
cd backend
python main_enhanced.py

echo.
echo Server process completed.
pause