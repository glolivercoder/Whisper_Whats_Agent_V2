#!/usr/bin/env python3
"""
Comprehensive test with torch.load patching for XTTS v2
"""

import os
import sys
import tempfile
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def setup_environment():
    """Setup environment variables for Coqui TTS"""
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['COQUI_TTS_NO_MECAB'] = '1'
    
    # Create a dummy mecabrc file to prevent the error
    try:
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
    """Apply comprehensive PyTorch compatibility fix"""
    try:
        import torch
        # Add safe globals for XTTS config to fix PyTorch 2.6+ compatibility issue
        try:
            from TTS.tts.configs.xtts_config import XttsConfig
            from TTS.tts.models.xtts import XttsAudioConfig
            from TTS.config.shared_configs import BaseDatasetConfig
            # Add all required classes to safe globals
            torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig])
            print("✅ Added XTTS config and related classes to safe globals for PyTorch compatibility")
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

def patch_torch_load():
    """Patch torch.load to bypass weights_only issue"""
    try:
        import torch
        original_load = torch.load
        
        def patched_load(f, map_location=None, pickle_module=None, *, weights_only=False, mmap=None, **pickle_load_args):
            # Force weights_only=False to bypass the issue
            return original_load(f, map_location, pickle_module, weights_only=False, mmap=mmap, **pickle_load_args)
        
        torch.load = patched_load
        print("✅ Patched torch.load to bypass weights_only issue")
        return True
    except Exception as e:
        print(f"⚠️ Failed to patch torch.load: {e}")
        return False

def restore_torch_load():
    """Restore original torch.load function"""
    try:
        import torch
        if hasattr(torch.load, '_original_load'):
            torch.load = torch.load._original_load
            print("✅ Restored original torch.load function")
    except Exception as e:
        print(f"⚠️ Failed to restore torch.load: {e}")

def test_xtts_v2_model_loading():
    """Test XTTS v2 model loading with comprehensive fixes"""
    print("\n🔄 Testing XTTS v2 model loading with comprehensive fixes...")
    
    try:
        # Apply all fixes
        setup_environment()
        apply_pytorch_compatibility_fix()
        monkey_patch_mecab()
        patch_torch_load()
        
        # Import with error suppression
        from io import StringIO
        import contextlib
        
        stderr_capture = StringIO()
        with contextlib.redirect_stderr(stderr_capture):
            from TTS.api import TTS
            
            # Load XTTS v2 model
            print("🔄 Loading XTTS v2 model...")
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                      progress_bar=False, gpu=False)
            print("✅ XTTS v2 model loaded successfully")
            
            # Check model properties
            print(f"ℹ️ Model class: {tts.__class__.__name__}")
            
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
                restore_torch_load()
                return True
            else:
                print("❌ Basic speech synthesis failed")
                restore_torch_load()
                return False
                
    except Exception as e:
        print(f"❌ XTTS v2 model loading failed: {e}")
        restore_torch_load()
        return False

def test_voice_cloning_functionality():
    """Test voice cloning functionality with comprehensive fixes"""
    print("\n🎭 Testing voice cloning functionality...")
    
    try:
        # Apply all fixes
        setup_environment()
        apply_pytorch_compatibility_fix()
        monkey_patch_mecab()
        patch_torch_load()
        
        # Import with error suppression
        from io import StringIO
        import contextlib
        
        stderr_capture = StringIO()
        with contextlib.redirect_stderr(stderr_capture):
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
                restore_torch_load()
                return True
            else:
                print("❌ Voice cloning failed")
                os.unlink(temp_path)
                if os.path.exists(output_path):
                    os.unlink(output_path)
                restore_torch_load()
                return False
                
    except Exception as e:
        print(f"❌ Voice cloning test failed: {e}")
        restore_torch_load()
        return False

def main():
    """Main test function"""
    print("🎯 XTTS v2 Comprehensive Test")
    print("=" * 35)
    
    # Test model loading
    model_ok = test_xtts_v2_model_loading()
    
    if not model_ok:
        print("\n❌ XTTS v2 model loading failed.")
        return False
    
    # Test voice cloning
    cloning_ok = test_voice_cloning_functionality()
    
    if not cloning_ok:
        print("\n❌ Voice cloning test failed.")
        return False
    
    print("\n🎉 All tests passed! XTTS v2 should work correctly with all fixes applied.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)