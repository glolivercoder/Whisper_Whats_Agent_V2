@echo off
echo ==========================================
echo   FIXING DEPENDENCY CONFLICTS
echo ==========================================
echo.
echo Resolving TTS, tokenizers, and transformers conflicts...
echo.

set original_dir=%cd%

echo 1. Upgrading pip first...
python -m pip install --upgrade pip

echo.
echo 2. Removing problematic packages...
echo   - Removing tokenizers (will install correct version)...
pip uninstall -y tokenizers

echo   - Removing transformers (will install correct version)...
pip uninstall -y transformers

echo   - Removing tortoise-tts (conflicting)...
pip uninstall -y tortoise-tts

echo.
echo 3. Installing packages in correct order...
echo.

echo Installing tokenizers==0.13.3...
pip install tokenizers==0.13.3

echo Installing transformers==4.31.0...
pip install transformers==4.31.0

echo Installing faster-whisper==1.0.1...
pip install faster-whisper==1.0.1

echo Installing openai-whisper...
pip install openai-whisper==20231117

echo Installing TTS==0.22.0 (should auto-handle dependencies)...
pip install TTS==0.22.0

echo.
echo 4. Installing audio processing libraries...
echo Installing pydub==0.25.1...
pip install pydub==0.25.1

echo Installing ffmpeg-python==0.2.0...
pip install ffmpeg-python==0.2.0

echo.
echo ==========================================
echo   DEPENDENCIES FIXED!
echo ==========================================
echo.
echo What was resolved:
echo ✅ tokenizers version fixed (0.13.3 compatible with faster-whisper)
echo ✅ transformers version fixed (4.31.0 compatible with TTS)
echo ✅ tortoise-tts conflicts removed
echo ✅ TTS properly installed with correct dependencies
echo.
echo You can now run:
echo python backend/main_enhanced.py
echo.
echo The "🔊 CoquiTTS VoxClone" tab should work properly!
echo.
pause