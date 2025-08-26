#!/usr/bin/env python3
"""
Test XTTS v2 voice cloning with a real reference audio file
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
    
    # Test basic synthesis with default speaker
    print("\n🔄 Testing basic speech synthesis with default speaker...")
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
            print("✅ Basic speech synthesis with default speaker works")
            os.unlink(temp_path)
        else:
            print("❌ Basic speech synthesis with default speaker failed")
    except Exception as e:
        print(f"❌ Basic speech synthesis failed: {e}")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    # Test voice cloning with real reference audio
    print("\n🔄 Testing voice cloning with real reference audio...")
    
    # Check if test reference audio exists
    ref_audio_path = "test_reference.wav"
    if not os.path.exists(ref_audio_path):
        print("❌ Reference audio file not found. Please run create_test_audio.py first.")
        sys.exit(1)
    
    print(f"🎵 Using reference audio: {ref_audio_path}")
    
    temp_file2 = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path2 = temp_file2.name
    temp_file2.close()
    
    try:
        # This is the key test - using speaker_wav parameter for voice cloning
        tts.tts_to_file(
            text="Olá, esta é uma voz clonada com XTTS v2.",
            file_path=temp_path2,
            speaker_wav=ref_audio_path,  # This is the key parameter for voice cloning
            language="pt"
        )
        
        if os.path.exists(temp_path2) and os.path.getsize(temp_path2) > 0:
            print("✅ Voice cloning with reference audio works!")
            print("✅ XTTS v2 voice cloning is functioning correctly")
            os.unlink(temp_path2)
        else:
            print("❌ Voice cloning with reference audio failed")
    except Exception as e:
        print(f"❌ Voice cloning failed: {e}")
        import traceback
        traceback.print_exc()
        if os.path.exists(temp_path2):
            os.unlink(temp_path2)
    
    print("\n✅ XTTS v2 voice cloning test completed")
    
except Exception as e:
    print(f"❌ Failed to test XTTS v2 model: {e}")
    import traceback
    traceback.print_exc()