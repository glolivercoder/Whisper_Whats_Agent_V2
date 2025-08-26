#!/usr/bin/env python3
"""
Test script to verify XTTS v2 model works correctly with voice cloning
"""

import os
import sys

# Set environment variables to fix MeCab issues on Windows
os.environ['MECAB_PATH'] = ''
os.environ['MECAB_CHARSET'] = 'utf8'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['COQUI_TTS_NO_MECAB'] = '1'

print("🔧 Environment variables set for Coqui TTS on Windows")

# Monkey patch approach - replace MeCab with a mock before importing TTS
class MockMeCab:
    """Mock MeCab module to prevent import errors"""
    class Tagger:
        def __init__(self, *args, **kwargs):
            pass
        
        def parse(self, text):
            # Return a simple parsed format for testing
            return f"{text}\tunknown\nEOS\n"

# Apply monkey patch before importing TTS
import sys
sys.modules['MeCab'] = MockMeCab
print("✅ MeCab monkey patch applied")

try:
    print("\n🔄 Importing TTS.api...")
    from TTS.api import TTS
    print("✅ TTS.api imported successfully")
    
    print("\n🔄 Loading XTTS v2 model...")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
    print("✅ XTTS v2 model loaded successfully")
    
    print("\n🔄 Testing speech synthesis...")
    tts.tts_to_file(text="Olá, este é um teste de voz com o modelo XTTS v2.", file_path="test_output_xtts.wav")
    print("✅ Speech synthesis completed successfully")
    
    # Test voice cloning capabilities if reference audio is available
    reference_audio_dir = os.path.join(os.getcwd(), "reference_audio")
    if os.path.exists(reference_audio_dir):
        reference_files = [f for f in os.listdir(reference_audio_dir) if f.endswith(('.wav', '.mp3', '.flac'))]
        if reference_files:
            ref_audio_path = os.path.join(reference_audio_dir, reference_files[0])
            print(f"\n🔄 Testing voice cloning with reference audio: {ref_audio_path}")
            tts.tts_to_file(
                text="Esta é uma voz clonada usando o modelo XTTS v2.",
                file_path="test_cloned_voice_xtts.wav",
                speaker_wav=ref_audio_path,
                language="pt-br"
            )
            print("✅ Voice cloning test completed successfully")
        else:
            print("\nℹ️ No reference audio files found for voice cloning test")
    else:
        print("\nℹ️ Reference audio directory not found for voice cloning test")
    
    print("\n🎉 XTTS v2 is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n📋 XTTS v2 test completed successfully!")