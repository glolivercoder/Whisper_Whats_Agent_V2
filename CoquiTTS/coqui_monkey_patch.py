#!/usr/bin/env python3
"""
Monkey patch approach to fix Coqui TTS MeCab issue on Windows
"""

import os
import sys

# Set environment variables to fix MeCab issues on Windows
os.environ['MECAB_PATH'] = ''
os.environ['MECAB_CHARSET'] = 'utf8'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['COQUI_TTS_NO_MECAB'] = '1'

print("🔧 Environment variables set for Coqui TTS on Windows")

# Add the CoquiTTS directory to the path
coqui_dir = os.path.join(os.path.dirname(__file__))
project_root = os.path.dirname(coqui_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Monkey patch approach - replace MeCab with a mock before importing TTS
class MockMeCab:
    """Mock MeCab module to prevent import errors"""
    class Tagger:
        def __init__(self, *args, **kwargs):
            pass
        
        def parse(self, text):
            # Return a simple parsed format for testing
            return f"{text}\tunknown\nEOS\n"

# Try to patch MeCab before importing TTS
try:
    import sys
    sys.modules['MeCab'] = MockMeCab
    print("✅ MeCab monkey patch applied")
except Exception as e:
    print(f"⚠️ Could not apply MeCab monkey patch: {e}")

try:
    print("\n🔄 Importing TTS.api...")
    from TTS.api import TTS
    print("✅ TTS.api imported successfully")
    
    print("\n🔄 Loading Portuguese VITS model...")
    tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)
    print("✅ Portuguese VITS model loaded successfully")
    
    print("\n🔄 Testing speech synthesis...")
    tts.tts_to_file(text="Olá, este é um teste de voz.", file_path="test_output.wav")
    print("✅ Speech synthesis completed successfully")
    
    print("\n🎉 Coqui TTS is working correctly with the monkey patch!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Try alternative models
    models_to_try = [
        "tts_models/multilingual/multi-dataset/your_tts",
        "tts_models/pt/cv/tacotron2-DDC",
        "tts_models/en/ljspeech/tacotron2-DDC"
    ]
    
    for model_name in models_to_try:
        try:
            print(f"\n🔄 Trying alternative model: {model_name}")
            tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
            tts.tts_to_file(text="Teste de voz.", file_path="test_output.wav")
            print(f"✅ Alternative model {model_name} works!")
            break
        except Exception as e2:
            print(f"❌ Failed to load {model_name}: {e2}")
            continue
    else:
        print("\n❌ No models working")
        sys.exit(1)

print("\n📋 Test completed successfully!")