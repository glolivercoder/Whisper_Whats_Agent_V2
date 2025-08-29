@echo off
echo ========================================
echo  INSTALL TTS VOICE CLONE DEPENDENCIES
echo ========================================
echo.
echo Installing CoquiTTS VoxClone dependencies...
echo.

echo 1. Installing TTS Library...
pip install TTS==0.22.0

echo.
echo 2. Installing Audio Processing...
pip install pydub==0.25.1

echo.
echo 3. Installing FFmpeg for audio conversion...
pip install ffmpeg-python==0.2.0

echo.
echo 4. Installing additional audio tools...
pip install soundfile librosa

echo.
echo ========================================
echo    DEPENDENCIES INSTALLED!
echo ========================================
echo.
echo TTS VoxClone Features:
echo ✨ Text-to-Speech Synthesis
echo 🗣️  Voice Cloning with Reference Audio
echo 👥  Voice Profile Management
echo 🔊 Multiple Audio Formats (WAV/MP3/OGG)
echo 🎵 Multiple Models (XTTS v2, YourTTS, etc.)
echo.
echo Ready to use! Access the new "🔊 CoquiTTS VoxClone" tab.
echo.
echo For support, see: README_TTS_VOICE_CLONE.md
echo.
pause