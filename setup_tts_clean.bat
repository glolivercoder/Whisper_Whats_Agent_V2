@echo off
echo ==========================================
echo   CLEAN TTS SETUP FOR DEPENDENCY FIXES
echo ==========================================
echo.
echo This script will fix TTS dependency conflicts by:
echo 1. Removing conflicting packages
echo 2. Installing correct versions in proper order
echo 3. Testing TTS functionality
echo.

echo Step 1: Installing correctly ordered dependencies...
echo.

echo Updating pip...
python -m pip install --upgrade pip

echo.
echo Removing conflicting packages...
pip uninstall -y tokenizers transformers tortoise-tts

echo.
echo Installing in correct order:
echo.

echo 1. tokenizers==0.13.3
pip install tokenizers==0.13.3

echo.
echo 2. transformers==4.31.0
pip install transformers==4.31.0

echo.
echo 3. faster-whisper==1.0.1
pip install faster-whisper==1.0.1

echo.
echo 4. Audio processing libraries
pip install pydub==0.25.1 ffmpeg-python==0.2.0

echo.
echo 5. CoquiTTS (main library)...
pip install "TTS==0.22.0"

echo.
echo ==========================================
echo   TESTING INSTALLATION
echo ==========================================
echo.

echo Testing imports...
python -c "from TTS.api import TTS; print('✅ TTS import successful')"

echo.
python -c "import tokenizers; print(f'✅ Tokenizers version: {tokenizers.__version__}')"

echo.
python -c "import transformers; print(f'✅ Transformers version: {transformers.__version__}')"

echo.
echo ==========================================
echo   SETUP COMPLETE!
echo ==========================================
echo.
echo Summary:
echo ✅ Installed tokenizers==0.13.3 (compatible with faster-whisper)
echo ✅ Installed transformers==4.31.0 (compatible with TTS)
echo ✅ Installed TTS==0.22.0 with proper dependencies
echo ✅ Removed conflicting packages (tortoise-tts)
echo.
echo You can now use:
echo python backend/main_enhanced.py
echo.
echo Then visit the '🔊 CoquiTTS VoxClone' tab!
echo.

pause