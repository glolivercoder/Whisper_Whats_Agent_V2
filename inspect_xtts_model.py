#!/usr/bin/env python3
"""
Inspect XTTS v2 model properties to understand speaker handling
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
    
    # Inspect model properties
    print("\n🔍 Model Properties:")
    print(f"  Model name: {getattr(tts, 'name', 'N/A')}")
    print(f"  Model type: {type(tts)}")
    print(f"  Is multi-speaker: {getattr(tts, 'is_multi_speaker', 'N/A')}")
    print(f"  Has speakers list: {hasattr(tts, 'speakers')}")
    if hasattr(tts, 'speakers'):
        print(f"  Speakers: {getattr(tts, 'speakers', 'N/A')}")
    
    # Check available methods and attributes
    print("\n🔍 Available methods and attributes:")
    attrs = [attr for attr in dir(tts) if not attr.startswith('_')]
    for attr in sorted(attrs):
        try:
            value = getattr(tts, attr)
            if not callable(value):
                print(f"  {attr}: {value}")
        except AttributeError:
            print(f"  {attr}: <AttributeError>")
        except Exception as e:
            print(f"  {attr}: <Error: {e}>")
    
    # Check tts_to_file method signature
    import inspect
    print("\n🔍 tts_to_file method signature:")
    try:
        sig = inspect.signature(tts.tts_to_file)
        print(f"  Parameters: {list(sig.parameters.keys())}")
        for name, param in sig.parameters.items():
            print(f"    {name}: {param}")
    except Exception as e:
        print(f"  Could not inspect signature: {e}")
        
    # Check if model has speaker embedding capability
    has_speaker_embedding = hasattr(tts, 'is_multi_speaker') and tts.is_multi_speaker
    print(f"\n🎤 Speaker embedding capability: {has_speaker_embedding}")
    
    # Check model config if available
    if hasattr(tts, 'config'):
        print("\n🔍 Model config:")
        config = tts.config
        print(f"  Config type: {type(config)}")
        if hasattr(config, 'model_args'):
            print(f"  Model args: {config.model_args}")
        if hasattr(config, 'speakers_file'):
            print(f"  Speakers file: {config.speakers_file}")
            
except Exception as e:
    print(f"❌ Failed to inspect XTTS v2 model: {e}")
    import traceback
    traceback.print_exc()