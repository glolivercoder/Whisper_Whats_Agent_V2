#!/usr/bin/env python3
"""
Final test script to verify XTTS v2 voice cloning functionality with complete fixes
"""

import os
import sys
import tempfile
import warnings
from io import StringIO
import contextlib

# Suppress warnings
warnings.filterwarnings("ignore")

def setup_environment():
    """Setup environment variables for Coqui TTS to bypass MeCab issues on Windows"""
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['COQUI_TTS_NO_MECAB'] = '1'
    
    # Create a dummy mecabrc file to prevent the error
    try:
        import tempfile
        temp_dir = tempfile.gettempdir()
        mecabrc_path = os.path.join(temp_dir, 'mecabrc')
        
        if not os.path.exists(mecabrc_path):
            with open(mecabrc_path, 'w') as f:
                f.write("# Dummy mecabrc file to prevent MeCab errors\n")
            print(f"✅ Created dummy mecabrc at {mecabrc_path}")
    except Exception as e:
        print(f"⚠️ Could not create dummy mecabrc: {e}")
    
    print("🔧 Environment variables set for Coqui TTS")

def apply_pytorch_compatibility_fix():
    """Apply complete PyTorch compatibility fix for XTTS v2 model loading"""
    try:
        import torch
        # Add safe globals for XTTS config to fix PyTorch 2.6+ compatibility issue
        try:
            from TTS.tts.configs.xtts_config import XttsConfig
            from TTS.tts.models.xtts import XttsAudioConfig
            torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])
            print("✅ Added XTTS config and audio config to safe globals for PyTorch compatibility")
            return True
        except Exception as e:
            print(f"ℹ️ Could not add XTTS config to safe globals: {e}")
            return False
    except ImportError:
        print("⚠️ PyTorch not available, skipping compatibility fix")
        return False

def monkey_patch_mecab():
    """Monkey patch MeCab to prevent import errors on Windows"""
    try:
        import sys
        
        # Mock MeCab module to prevent import errors
        class MockMeCab:
            """Mock MeCab module to prevent import errors"""
            class Tagger:
                def __init__(self, *args, **kwargs):
                    pass
                
                def parse(self, text):
                    # Return a simple parsed format for testing
                    return f"{text}\tunknown\nEOS\n"

        # Apply monkey patch before importing TTS
        sys.modules['MeCab'] = MockMeCab
        print("✅ Applied MeCab monkey patch")
        return True
    except Exception as e:
        print(f"⚠️ Failed to apply MeCab monkey patch: {e}")
        return False

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
    
    # Capture stderr to suppress MeCab error messages
    stderr_capture = StringIO()
    
    try:
        # Import TTS with error suppression
        with contextlib.redirect_stderr(stderr_capture):
            from TTS.api import TTS
            
            # Load XTTS v2 model with weights_only=False to bypass the issue
            print("🔄 Loading XTTS v2 model...")
            # Use the workaround for PyTorch 2.6+ compatibility
            import torch
            original_load = torch.load
            
            def patched_load(f, map_location=None, pickle_module=None, *, weights_only=False, mmap=None, **pickle_load_args):
                return original_load(f, map_location, pickle_module, weights_only=False, mmap=mmap, **pickle_load_args)
            
            torch.load = patched_load
            
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                      progress_bar=False, gpu=False)
                      
            # Restore original load function
            torch.load = original_load
            
            print("✅ XTTS v2 model loaded successfully")
            
            # Test voice cloning capabilities
            if hasattr(tts, 'is_multi_speaker') and tts.is_multi_speaker:
                print("✅ Model supports multi-speaker/voice cloning")
            else:
                print("⚠️ Model may not support voice cloning")
                
            # Test language support
            print("🌐 Checking language support...")
            try:
                # Try to list languages if supported
                if hasattr(tts, 'languages'):
                    print(f"🌐 Supported languages: {tts.languages}")
                else:
                    # Try alternative method
                    print("ℹ️  Model loaded, checking basic properties...")
                    print(f"ℹ️  Model name: {tts.__class__.__name__}")
            except Exception as e:
                print(f"ℹ️  Could not determine language support: {e}")
                
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
                return True
            else:
                print("❌ Basic speech synthesis failed")
                return False
                
    except Exception as e:
        # Log the captured stderr output for debugging
        captured_errors = stderr_capture.getvalue()
        if captured_errors and "MeCab" in captured_errors:
            print("ℹ️ MeCab warnings were suppressed (this is normal on Windows)")
        
        print(f"❌ XTTS v2 model test failed: {e}")
        return False

def test_voice_cloning():
    """Test voice cloning functionality"""
    print("\n🎭 Testing voice cloning functionality...")
    
    try:
        # Import TTS with error suppression
        stderr_capture = StringIO()
        with contextlib.redirect_stderr(stderr_capture):
            from TTS.api import TTS
            
            # Load XTTS v2 model with weights_only=False to bypass the issue
            import torch
            original_load = torch.load
            
            def patched_load(f, map_location=None, pickle_module=None, *, weights_only=False, mmap=None, **pickle_load_args):
                return original_load(f, map_location, pickle_module, weights_only=False, mmap=mmap, **pickle_load_args)
            
            torch.load = patched_load
            
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                      progress_bar=False, gpu=False)
                      
            # Restore original load function
            torch.load = original_load
        
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
        # XTTS v2 requires speaker_wav parameter for voice cloning
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

def check_model_details():
    """Check detailed information about the XTTS v2 model"""
    print("\n🔍 Checking XTTS v2 model details...")
    
    try:
        stderr_capture = StringIO()
        with contextlib.redirect_stderr(stderr_capture):
            from TTS.api import TTS
            
            # Load XTTS v2 model with weights_only=False to bypass the issue
            import torch
            original_load = torch.load
            
            def patched_load(f, map_location=None, pickle_module=None, *, weights_only=False, mmap=None, **pickle_load_args):
                return original_load(f, map_location, pickle_module, weights_only=False, mmap=mmap, **pickle_load_args)
            
            torch.load = patched_load
            
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                      progress_bar=False, gpu=False)
                      
            # Restore original load function
            torch.load = original_load
            
            # Print model information
            print(f"ℹ️ Model class: {tts.__class__.__name__}")
            print(f"ℹ️ Model type: {type(tts)}")
            
            # Check if it has specific XTTS attributes
            xtts_attrs = ['speakers', 'languages', 'speaker_manager']
            for attr in xtts_attrs:
                if hasattr(tts, attr):
                    print(f"✅ Has {attr} attribute")
                else:
                    print(f"❌ Missing {attr} attribute")
            
            # Try to list available speakers if possible
            try:
                if hasattr(tts, 'speakers') and tts.speakers:
                    print(f"🎤 Available speakers: {list(tts.speakers.keys())[:5]}...")  # Show first 5
                elif hasattr(tts, 'speaker_manager') and hasattr(tts.speaker_manager, 'speakers'):
                    speakers = tts.speaker_manager.speakers
                    print(f"🎤 Available speakers: {list(speakers.keys())[:5]}...")  # Show first 5
            except Exception as e:
                print(f"ℹ️ Could not list speakers: {e}")
                
            return True
            
    except Exception as e:
        print(f"❌ Failed to check model details: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 XTTS v2 Voice Cloning Test with Complete Fixes")
    print("=" * 55)
    
    # Setup environment
    setup_environment()
    
    # Apply PyTorch compatibility fix
    pytorch_fix = apply_pytorch_compatibility_fix()
    if not pytorch_fix:
        print("⚠️  Continuing without PyTorch compatibility fix...")
    
    # Apply MeCab monkey patch
    patch_ok = monkey_patch_mecab()
    if not patch_ok:
        print("⚠️  Continuing without MeCab patch...")
    
    # Test dependencies
    deps_ok = test_xtts_v2_dependencies()
    
    if not deps_ok:
        print("\n❌ Missing critical dependencies. Please install them.")
        return False
    
    # Check model details
    check_model_details()
    
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