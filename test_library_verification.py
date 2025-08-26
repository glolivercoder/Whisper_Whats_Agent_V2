#!/usr/bin/env python3
"""
Final library verification test for XTTS v2 voice cloning
"""

import os
import sys
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def setup_environment():
    """Setup environment variables for Coqui TTS"""
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['COQUI_TTS_NO_MECAB'] = '1'
    print("🔧 Environment variables set for Coqui TTS")

def test_core_libraries():
    """Test if all core libraries are installed"""
    print("🧪 Testing core libraries...")
    
    core_libraries = {
        'torch': 'PyTorch deep learning framework',
        'torchaudio': 'Audio processing with PyTorch',
        'TTS': 'Coqui TTS library',
        'librosa': 'Audio analysis library',
        'encodec': 'Audio encoding library',
        'numpy': 'Numerical computing',
        'scipy': 'Scientific computing'
    }
    
    missing_libs = []
    
    for lib, description in core_libraries.items():
        try:
            if lib == 'TTS':
                import TTS.api
            else:
                __import__(lib)
            print(f"✅ {lib} - {description}")
        except ImportError as e:
            print(f"❌ {lib} - MISSING: {e}")
            missing_libs.append(lib)
    
    return len(missing_libs) == 0

def test_optional_libraries():
    """Test if optional libraries are installed"""
    print("\n🧪 Testing optional libraries...")
    
    optional_libraries = {
        'deepspeed': 'Performance optimization',
        'soundfile': 'Audio file I/O',
        'soxr': 'Sample rate conversion',
        'inflect': 'Text processing',
        'unidecode': 'Unicode text processing'
    }
    
    missing_libs = []
    
    for lib, description in optional_libraries.items():
        try:
            __import__(lib)
            print(f"✅ {lib} - {description}")
        except ImportError as e:
            print(f"⚠️ {lib} - MISSING (optional): {e}")
            missing_libs.append(lib)
    
    if missing_libs:
        print(f"\nℹ️ {len(missing_libs)} optional libraries missing - this is acceptable")
    else:
        print("\n🎉 All optional libraries installed!")
    
    return True

def test_xtts_v2_model_access():
    """Test if XTTS v2 model files are accessible"""
    print("\n🧪 Testing XTTS v2 model access...")
    
    try:
        # Test if we can access the model manager
        from TTS.utils.manage import ModelManager
        manager = ModelManager()
        print("✅ ModelManager accessible")
        
        # Check if XTTS v2 model is listed
        model_names = manager.list_models()
        xtts_models = [name for name in model_names if 'xtts' in name.lower()]
        
        if xtts_models:
            print(f"✅ XTTS models found: {xtts_models}")
            return True
        else:
            print("⚠️ No XTTS models found in model list")
            return False
            
    except Exception as e:
        print(f"❌ Model access test failed: {e}")
        return False

def test_tts_api_functionality():
    """Test basic TTS API functionality"""
    print("\n🧪 Testing TTS API functionality...")
    
    try:
        from TTS.api import TTS
        print("✅ TTS API accessible")
        
        # List available models
        tts_instance = TTS()
        models = tts_instance.list_models()
        print(f"✅ {len(models)} models available")
        
        # Check for XTTS v2 specifically
        xtts_v2_models = [m for m in models if 'xtts_v2' in m]
        if xtts_v2_models:
            print(f"✅ XTTS v2 models available: {xtts_v2_models}")
            return True
        else:
            print("⚠️ XTTS v2 model not found in list")
            return False
            
    except Exception as e:
        print(f"❌ TTS API test failed: {e}")
        return False

def test_audio_processing_libraries():
    """Test audio processing libraries"""
    print("\n🧪 Testing audio processing libraries...")
    
    audio_libs = {
        'soundfile': 'Audio file I/O',
        'soxr': 'Sample rate conversion',
        'librosa': 'Audio analysis'
    }
    
    for lib, description in audio_libs.items():
        try:
            __import__(lib)
            print(f"✅ {lib} - {description}")
        except ImportError as e:
            print(f"❌ {lib} - MISSING: {e}")
            return False
    
    return True

def main():
    """Main verification function"""
    print("🎯 XTTS v2 Library Verification Test")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    # Test core libraries
    core_ok = test_core_libraries()
    
    if not core_ok:
        print("\n❌ Critical libraries missing. Voice cloning will not work.")
        return False
    
    # Test optional libraries
    optional_ok = test_optional_libraries()
    
    # Test model access
    model_access_ok = test_xtts_v2_model_access()
    
    # Test TTS API
    api_ok = test_tts_api_functionality()
    
    # Test audio processing
    audio_ok = test_audio_processing_libraries()
    
    print("\n" + "=" * 40)
    if core_ok and audio_ok:
        print("🎉 All critical libraries are present!")
        print("✅ XTTS v2 voice cloning should work with the current setup.")
        
        if model_access_ok and api_ok:
            print("✅ XTTS v2 model is accessible.")
        else:
            print("⚠️ XTTS v2 model access issues detected.")
            
        return True
    else:
        print("❌ Critical libraries missing. Voice cloning may not work properly.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)