#!/usr/bin/env python3
"""
Detailed test script for Coqui TTS to diagnose issues
"""

import os
import sys
import warnings
from io import StringIO

def test_coqui_import():
    """Test Coqui TTS import with detailed error reporting"""
    print("🔍 Testing Coqui TTS import...")
    
    # Set environment variables
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Suppress warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = captured_stderr = StringIO()
    
    try:
        print("🔄 Importing TTS.api...")
        from TTS.api import TTS
        print("✅ TTS.api imported successfully")
        
        # Try to load a Portuguese model
        print("🔄 Loading Portuguese VITS model...")
        tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)
        print("✅ Portuguese VITS model loaded successfully")
        
        # Test synthesis
        print("🔄 Testing speech synthesis...")
        tts.tts_to_file(text="Olá, este é um teste de voz.", file_path="test_output.wav")
        print("✅ Speech synthesis completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Show captured stderr
        captured_output = captured_stderr.getvalue()
        if captured_output:
            print(f"Captured stderr: {captured_output}")
        
        return False
    finally:
        sys.stderr = old_stderr

def test_alternative_models():
    """Test alternative models that might work better"""
    models_to_try = [
        "tts_models/pt/cv/vits",
        "tts_models/multilingual/multi-dataset/your_tts",
        "tts_models/pt/cv/tacotron2-DDC"
    ]
    
    # Set environment variables
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Suppress warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    # Capture stderr
    old_stderr = sys.stderr
    sys.stderr = captured_stderr = StringIO()
    
    try:
        from TTS.api import TTS
        
        for model_name in models_to_try:
            try:
                print(f"🔄 Trying model: {model_name}")
                tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
                print(f"✅ Model {model_name} loaded successfully")
                
                # Test synthesis
                tts.tts_to_file(text="Teste de voz.", file_path="test_output.wav")
                print(f"✅ Synthesis with {model_name} completed successfully")
                return True
                
            except Exception as e:
                print(f"❌ Failed to load {model_name}: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ Error importing TTS: {e}")
        return False
    finally:
        sys.stderr = old_stderr

if __name__ == "__main__":
    print("🧪 Detailed Coqui TTS Test")
    print("=" * 40)
    
    print("\n1. Testing direct import and Portuguese model:")
    success1 = test_coqui_import()
    
    if not success1:
        print("\n2. Testing alternative models:")
        success2 = test_alternative_models()
        
        if success2:
            print("\n🎉 Alternative model works!")
        else:
            print("\n❌ No models working")
    else:
        print("\n🎉 Coqui TTS is working correctly!")
    
    print("\n📋 Test completed")