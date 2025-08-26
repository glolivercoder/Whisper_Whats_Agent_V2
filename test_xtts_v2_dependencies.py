#!/usr/bin/env python3
"""
Test script to verify XTTS v2 voice cloning functionality with all dependencies
"""

import os
import sys
import tempfile
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

def test_xtts_v2_dependencies():
    """Test if all required dependencies for XTTS v2 are installed"""
    print("🧪 Testing XTTS v2 dependencies...")
    
    dependencies = {
        'torch': 'PyTorch for deep learning',
        'torchaudio': 'Audio processing',
        'librosa': 'Audio analysis',
        'encodec': 'Audio encoding',
        'deepspeed': 'Performance optimization',
        'numpy': 'Numerical computing',
        'scipy': 'Scientific computing'
    }
    
    missing_deps = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep} - {description}")
        except ImportError as e:
            print(f"❌ {dep} - MISSING: {e}")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
        return False
    else:
        print("\n🎉 All dependencies are installed!")
        return True

def test_xtts_v2_model():
    """Test XTTS v2 model loading and voice cloning"""
    print("\n🔄 Testing XTTS v2 model...")
    
    try:
        # Import TTS
        from TTS.api import TTS
        
        # Load XTTS v2 model
        print("🔄 Loading XTTS v2 model...")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                  progress_bar=False, gpu=False)
        print("✅ XTTS v2 model loaded successfully")
        
        # Test voice cloning capabilities
        if hasattr(tts, 'is_multi_speaker') and tts.is_multi_speaker:
            print("✅ Model supports multi-speaker/voice cloning")
        else:
            print("⚠️ Model may not support voice cloning")
            
        # Test language support
        if hasattr(tts, 'languages'):
            print(f"🌐 Supported languages: {tts.languages}")
        else:
            print("⚠️ Could not determine supported languages")
            
        # Test basic synthesis
        print("🔄 Testing basic speech synthesis...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            temp_path = tmp_file.name
            
        tts.tts_to_file(
            text="Olá, este é um teste de voz com XTTS v2.",
            file_path=temp_path,
            language="pt"
        )
        
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            print("✅ Basic speech synthesis works")
            os.unlink(temp_path)
        else:
            print("❌ Basic speech synthesis failed")
            
        return True
        
    except Exception as e:
        print(f"❌ XTTS v2 model test failed: {e}")
        return False

def test_voice_cloning():
    """Test voice cloning functionality"""
    print("\n🎭 Testing voice cloning functionality...")
    
    try:
        from TTS.api import TTS
        
        # Load XTTS v2 model
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                  progress_bar=False, gpu=False)
        
        # Create a simple test audio (in practice, you would use a real reference audio)
        print("🔄 Creating test audio for voice cloning...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            temp_path = tmp_file.name
            
        # Generate a base audio to use as reference
        tts.tts_to_file(
            text="Este é um áudio de referência para clonagem de voz.",
            file_path=temp_path,
            language="pt"
        )
        
        # Now try to use it for voice cloning
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as output_file:
            output_path = output_file.name
            
        print("🔄 Testing voice cloning with reference audio...")
        tts.tts_to_file(
            text="Esta é uma voz clonada usando XTTS v2.",
            file_path=output_path,
            speaker_wav=temp_path,
            language="pt"
        )
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print("✅ Voice cloning works")
            os.unlink(temp_path)
            os.unlink(output_path)
            return True
        else:
            print("❌ Voice cloning failed")
            os.unlink(temp_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
            return False
            
    except Exception as e:
        print(f"❌ Voice cloning test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 XTTS v2 Voice Cloning Test")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    # Test dependencies
    deps_ok = test_xtts_v2_dependencies()
    
    if not deps_ok:
        print("\n❌ Missing critical dependencies. Please install them.")
        return False
    
    # Test model
    model_ok = test_xtts_v2_model()
    
    if not model_ok:
        print("\n❌ XTTS v2 model test failed.")
        return False
    
    # Test voice cloning
    cloning_ok = test_voice_cloning()
    
    if not cloning_ok:
        print("\n❌ Voice cloning test failed.")
        return False
    
    print("\n🎉 All tests passed! XTTS v2 voice cloning should work correctly.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)