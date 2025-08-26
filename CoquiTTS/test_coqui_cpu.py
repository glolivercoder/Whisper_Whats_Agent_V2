#!/usr/bin/env python3
"""
Test script for Coqui TTS with CPU optimization
"""

import os
import sys
import time

# Apply MeCab fixes before any TTS imports
def apply_mecab_fixes():
    """Apply MeCab fixes for Windows"""
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("✅ MeCab environment fixes applied")

# Apply fixes immediately
apply_mecab_fixes()

try:
    from TTS.api import TTS
    import torch
    print("✅ Coqui TTS imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Coqui TTS: {e}")
    sys.exit(1)

def test_models():
    """Test different Coqui TTS models for Portuguese"""
    models_to_test = [
        "tts_models/multilingual/multi-dataset/xtts_v2",
        "tts_models/pt/cv/vits",
        "tts_models/multilingual/multi-dataset/your_tts"
    ]
    
    test_text = "Olá, este é um teste de síntese de voz em português brasileiro."
    
    for model_name in models_to_test:
        print(f"\n🔄 Testing model: {model_name}")
        try:
            start_time = time.time()
            
            # Initialize TTS with CPU optimization
            tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
            
            init_time = time.time() - start_time
            print(f"✅ Model loaded in {init_time:.2f} seconds")
            
            # Test synthesis
            syn_start = time.time()
            wav = tts.tts(text=test_text, language="pt")
            syn_time = time.time() - syn_start
            print(f"✅ Synthesis completed in {syn_time:.2f} seconds")
            print(f"📊 Total time: {init_time + syn_time:.2f} seconds")
            
            # Cleanup
            del tts
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
        except Exception as e:
            print(f"❌ Failed to test {model_name}: {e}")

if __name__ == "__main__":
    print("🚀 Coqui TTS CPU Performance Test")
    print("=" * 50)
    test_models()
    print("\n🏁 Test completed")