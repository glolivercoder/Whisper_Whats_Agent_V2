#!/usr/bin/env python3
"""
Test script to check XTTS v2 model loading with monkey patch and PyTorch compatibility fix
"""

import os
import sys

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
    print(f"Is multi-speaker: {hasattr(tts, 'is_multi_speaker') and tts.is_multi_speaker}")
    
    if hasattr(tts, 'speakers'):
        print(f"Available speakers: {getattr(tts, 'speakers', 'N/A')}")
    
    # Test basic synthesis without speaker (using default speaker)
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    print("🔄 Testing basic speech synthesis with default speaker...")
    tts.tts_to_file(
        text="Olá, este é um teste de voz com XTTS v2.",
        file_path=temp_path,
        language="pt"
    )
    
    import os
    if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
        print("✅ Basic speech synthesis with default speaker works")
        os.unlink(temp_path)
    else:
        print("❌ Basic speech synthesis with default speaker failed")
        
except Exception as e:
    print(f"❌ Failed to load XTTS v2 model: {e}")
    import traceback
    traceback.print_exc()