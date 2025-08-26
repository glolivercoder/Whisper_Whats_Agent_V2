#!/usr/bin/env python3
"""
Safe import wrapper for Coqui TTS that handles MeCab issues on Windows
"""

import os
import sys
import warnings
from io import StringIO

def setup_coqui_environment():
    """Setup environment variables to prevent MeCab issues"""
    # Set environment variables to bypass MeCab issues on Windows
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['COQUI_TTS_NO_MECAB'] = '1'
    
    # Try to disable MeCab-related warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    print("🔧 Coqui TTS environment configured")
    return True

def safe_import_tts():
    """Safely import TTS with MeCab error handling"""
    # Setup environment first
    setup_coqui_environment()
    
    # Capture stderr to suppress MeCab error messages
    old_stderr = sys.stderr
    sys.stderr = captured_stderr = StringIO()
    
    try:
        # Import TTS
        import TTS.api
        print("✅ TTS.api imported successfully")
        
        # Restore stderr
        sys.stderr = old_stderr
        
        # Show any captured output at debug level
        captured_output = captured_stderr.getvalue()
        if captured_output and "MeCab" in captured_output:
            print("ℹ️ MeCab warnings were suppressed (this is normal on Windows)")
            
        return TTS.api
        
    except Exception as e:
        # Restore stderr
        sys.stderr = old_stderr
        
        print(f"❌ TTS import error: {e}")
        return None

def load_model_safely(model_name="tts_models/pt/cv/vits"):
    """Safely load a Coqui TTS model"""
    TTS_api = safe_import_tts()
    
    if TTS_api is None:
        print("❌ Cannot load model - TTS not available")
        return None
    
    try:
        print(f"🔄 Loading model: {model_name}")
        tts = TTS_api.TTS(
            model_name=model_name,
            progress_bar=False,
            gpu=False
        )
        print(f"✅ Model loaded successfully: {model_name}")
        return tts
    except Exception as e:
        print(f"❌ Failed to load model {model_name}: {e}")
        return None

def test_coqui_tts():
    """Test Coqui TTS functionality"""
    print("🧪 Testing Coqui TTS...")
    
    # Models to try in order of preference
    models_to_try = [
        "tts_models/pt/cv/vits",  # Portuguese VITS
        "tts_models/multilingual/multi-dataset/your_tts",  # Multilingual
        "tts_models/pt/cv/tacotron2-DDC",  # Portuguese Tacotron2
        "tts_models/en/ljspeech/tacotron2-DDC"  # English fallback
    ]
    
    tts = None
    for model_name in models_to_try:
        tts = load_model_safely(model_name)
        if tts is not None:
            break
    
    if tts is None:
        print("❌ No models could be loaded")
        return False
    
    # Test synthesis
    try:
        print("🔄 Testing speech synthesis...")
        tts.tts_to_file(text="Olá, este é um teste de voz.", file_path="test_output.wav")
        print("✅ Speech synthesis completed successfully")
        return True
    except Exception as e:
        print(f"❌ Speech synthesis failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Safe Coqui TTS Import Test")
    print("=" * 30)
    
    success = test_coqui_tts()
    
    if success:
        print("\n🎉 Coqui TTS is working correctly!")
    else:
        print("\n❌ Coqui TTS is not working")
        sys.exit(1)