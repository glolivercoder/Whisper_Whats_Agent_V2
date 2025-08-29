#!/usr/bin/env python3
"""
Test the language code fix for XTTS v2 model
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
    
    # Check available languages
    available_languages = []
    if hasattr(tts, 'languages') and tts.languages:
        available_languages = tts.languages
    elif hasattr(tts, 'tts') and hasattr(tts.tts, 'languages') and tts.tts.languages:
        available_languages = tts.tts.languages
    
    print(f"🌍 Available languages: {available_languages}")
    
    # Test with different language codes
    import tempfile
    
    # Test 1: Using 'pt' (should work according to error message)
    print("\n🔄 Testing with language='pt'...")
    temp_file1 = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path1 = temp_file1.name
    temp_file1.close()
    
    try:
        tts.tts_to_file(
            text="Olá, este é um teste de voz.",
            file_path=temp_path1,
            language="pt"
        )
        
        if os.path.exists(temp_path1) and os.path.getsize(temp_path1) > 0:
            print("✅ Language 'pt' works")
            os.unlink(temp_path1)
        else:
            print("❌ Language 'pt' failed")
    except Exception as e:
        print(f"❌ Language 'pt' failed: {e}")
        if os.path.exists(temp_path1):
            os.unlink(temp_path1)
    
    # Test 2: Using 'pt-br' (should work according to error message)
    print("\n🔄 Testing with language='pt-br'...")
    temp_file2 = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path2 = temp_file2.name
    temp_file2.close()
    
    try:
        tts.tts_to_file(
            text="Olá, este é um teste de voz.",
            file_path=temp_path2,
            language="pt-br"
        )
        
        if os.path.exists(temp_path2) and os.path.getsize(temp_path2) > 0:
            print("✅ Language 'pt-br' works")
            os.unlink(temp_path2)
        else:
            print("❌ Language 'pt-br' failed")
    except Exception as e:
        print(f"❌ Language 'pt-br' failed: {e}")
        if os.path.exists(temp_path2):
            os.unlink(temp_path2)
    
    print("\n✅ Language code test completed")
    
except Exception as e:
    print(f"❌ Failed to test language codes: {e}")
    import traceback
    traceback.print_exc()