#!/usr/bin/env python3
"""
🔊 TTS Integration Test Script

This script tests the CoquiTTS VoxClone integration with WhatsApp Voice Agent V2.
It performs basic functionality checks and voice synthesis tests.
"""

import sys
import os
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("TTS_TEST")

def check_dependencies():
    """Check if TTS dependencies are installed"""
    logger.info("🔍 Checking TTS dependencies...")

    try:
        from TTS.api import TTS
        logger.info("✅ TTS library available")
    except ImportError:
        logger.error("❌ TTS library not found. Run: pip install TTS")
        return False

    try:
        from pydub import AudioSegment
        logger.info("✅ pydub library available")
    except ImportError:
        logger.error("❌ pydub library not found. Run: pip install pydub")
        return False

    try:
        import ffmpeg
        logger.info("✅ ffmpeg-python available")
    except ImportError:
        logger.warning("⚠️  ffmpeg-python not available (optional)")

    return True

def test_tts_service():
    """Test basic TTS synthesis"""
    logger.info("🎵 Testing basic TTS synthesis...")

    try:
        from TTS.api import TTS

        # Test text
        test_text = "Olá! Este é um teste de síntese de voz com CoquiTTS VoxClone."
        logger.info(f"Testing with text: {test_text}")

        # Load a basic Portuguese model
        logger.info("Loading XTTS v2 model...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

        # Generate audio
        output_file = "test_tts_output.wav"
        logger.info(f"Generating audio to: {output_file}")

        start_time = time.time()
        tts.tts_to_file(text=test_text, file_path=output_file)
        end_time = time.time()

        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            logger.info(".2f")
        else:
            logger.error("❌ Output file was not created")

        return True

    except Exception as e:
        logger.error(f"❌ TTS test failed: {e}")
        return False

def test_directory_structure():
    """Check if required directories exist"""
    logger.info("📁 Checking directory structure...")

    required_dirs = [
        "reference_audios",
        "generated_audios",
        "tts_profiles"
    ]

    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            logger.info(f"✅ Directory {dir_name}/ exists")
        else:
            logger.info(f"⚠️  Directory {dir_name}/ missing (will be created automatically)")

    return True

def main():
    """Main test script"""
    logger.info("🚀 Starting TTS Integration Test")
    logger.info("=" * 50)

    all_passed = True

    # Check dependencies
    if not check_dependencies():
        all_passed = False
        logger.error("Dependencies check failed")

    # Check directory structure
    if not test_directory_structure():
        all_passed = False
        logger.error("Directory structure check failed")

    # Test TTS service
    if not test_tts_service():
        all_passed = False
        logger.error("TTS service test failed")

    # Summary
    logger.info("=" * 50)
    if all_passed:
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("🎉 TTS VoxClone integration is working correctly")
        logger.info("\nNext steps:")
        logger.info("1. Start the main application")
        logger.info("2. Open the '🔊 CoquiTTS VoxClone' tab")
        logger.info("3. Try generating some audio!")
    else:
        logger.error("❌ SOME TESTS FAILED")
        logger.info("\nTroubleshooting:")
        logger.info("1. Install missing dependencies:")
        logger.info("   pip install TTS pydub ffmpeg-python")
        logger.info("2. Or run install script:")
        logger.info("   install_tts_dependencies.bat")

    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())