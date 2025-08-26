#!/usr/bin/env python3
"""
Test script to verify Coqui TTS fix on Windows
"""

import os
import sys

# Set environment variables to fix MeCab issues on Windows
os.environ['MECAB_PATH'] = ''
os.environ['MECAB_CHARSET'] = 'utf8'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['COQUI_TTS_NO_MECAB'] = '1'

print("🔧 Environment variables set for Coqui TTS on Windows")
print(f"MECAB_PATH: '{os.environ.get('MECAB_PATH', 'Not set')}'")
print(f"MECAB_CHARSET: '{os.environ.get('MECAB_CHARSET', 'Not set')}'")
print(f"COQUI_TTS_NO_MECAB: '{os.environ.get('COQUI_TTS_NO_MECAB', 'Not set')}'")

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
    
    print("\n🎉 Coqui TTS is working correctly with the fix!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    
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