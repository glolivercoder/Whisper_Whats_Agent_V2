#!/usr/bin/env python3
"""
Test script to verify XTTS v2 voice cloning fix
"""

import os
import sys
import tempfile

# Set environment variables to bypass MeCab issues on Windows
os.environ['MECAB_PATH'] = ''
os.environ['MECAB_CHARSET'] = 'utf8'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['COQUI_TTS_NO_MECAB'] = '1'

# Apply PyTorch compatibility fix for XTTS v2 model loading
try:
    import torch
    # Add safe globals for XTTS config to fix PyTorch 2.6+ compatibility issue
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
    from TTS.config.shared_configs import BaseDatasetConfig
    # Add all required classes to safe globals
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, XttsArgs, BaseDatasetConfig])
    print("✅ Added XTTS config and related classes to safe globals for PyTorch compatibility")
except Exception as e:
    print(f"ℹ️ Could not add XTTS config to safe globals: {e}")

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
sys.modules['MeCab'] = MockMeCab

try:
    # Import TTS API
    import TTS.api
    
    print("🔄 Loading XTTS v2 model...")
    tts = TTS.api.TTS(
        model_name="tts_models/multilingual/multi-dataset/xtts_v2",
        progress_bar=False,
        gpu=False
    )
    
    print(f"✅ Model loaded successfully: {tts.__class__.__name__}")
    
    # Check tts_to_file method signature
    import inspect
    print("\n🔍 tts_to_file method signature:")
    try:
        sig = inspect.signature(tts.tts_to_file)
        print(f"  Parameters: {list(sig.parameters.keys())}")
    except Exception as e:
        print(f"  Could not inspect signature: {e}")
    
    # Test basic synthesis
    print("\n🔄 Testing basic speech synthesis...")
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    try:
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
    except Exception as e:
        print(f"❌ Basic speech synthesis failed: {e}")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    # Test synthesis with speaker_wav parameter
    print("\n🔄 Testing speech synthesis with speaker_wav parameter...")
    
    # Create a dummy reference audio file
    ref_temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    ref_temp_path = ref_temp_file.name
    ref_temp_file.close()
    
    # Write some dummy data to make it a valid file
    with open(ref_temp_path, 'wb') as f:
        f.write(b"RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00")
    
    temp_file2 = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path2 = temp_file2.name
    temp_file2.close()
    
    try:
        # This is the key test - using speaker_wav parameter for voice cloning
        tts.tts_to_file(
            text="Olá, esta é uma voz clonada com XTTS v2.",
            file_path=temp_path2,
            speaker_wav=ref_temp_path,  # This is the key parameter for voice cloning
            language="pt"
        )
        
        if os.path.exists(temp_path2) and os.path.getsize(temp_path2) > 0:
            print("✅ Speech synthesis with speaker_wav (voice cloning) works")
            os.unlink(temp_path2)
        else:
            print("❌ Speech synthesis with speaker_wav failed")
    except Exception as e:
        print(f"❌ Speech synthesis with speaker_wav failed: {e}")
        import traceback
        traceback.print_exc()
        if os.path.exists(temp_path2):
            os.unlink(temp_path2)
    
    # Cleanup
    if os.path.exists(ref_temp_path):
        os.unlink(ref_temp_path)
        
    print("\n✅ XTTS v2 voice cloning test completed")
    
except Exception as e:
    print(f"❌ Failed to test XTTS v2 model: {e}")
    import traceback
    traceback.print_exc()