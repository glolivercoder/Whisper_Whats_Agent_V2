#!/usr/bin/env python3
"""
Test the exact method used in the application
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
    
    # Check model properties the same way as in the application
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # Better detection for multi-speaker models (same as in application)
    is_multi_speaker = False
    available_speakers = []
    
    # Check for speakers in different ways
    if hasattr(tts.tts, 'speakers') and tts.tts.speakers:
        is_multi_speaker = True
        available_speakers = tts.tts.speakers
    elif hasattr(tts.tts, 'speaker_manager') and hasattr(tts.tts.speaker_manager, 'speaker_ids'):
        if tts.tts.speaker_manager.speaker_ids:
            is_multi_speaker = True
            available_speakers = tts.tts.speaker_manager.speaker_ids
    elif "your_tts" in model_name.lower() or "xtts" in model_name.lower():
        # These models are known to be multi-speaker
        is_multi_speaker = True
        # For YourTTS, we know it has default speakers
        if "your_tts" in model_name.lower():
            available_speakers = ["default", "p225", "p226", "p227"]  # Common YourTTS speakers
    
    # Better detection for multi-lingual models (same as in application)
    is_multi_lingual = False
    available_languages = []
    
    # Check for language support in different ways
    if hasattr(tts.tts, 'language_manager') and tts.tts.language_manager:
        if hasattr(tts.tts.language_manager, 'language_ids'):
            available_languages = tts.tts.language_manager.language_ids
            is_multi_lingual = len(available_languages) > 1
    elif hasattr(tts.tts, 'languages') and tts.tts.languages:
        available_languages = tts.tts.languages
        is_multi_lingual = len(available_languages) > 1
    elif "multilingual" in model_name.lower() or "your_tts" in model_name.lower() or "xtts" in model_name.lower():
        # These models are known to be multi-lingual
        is_multi_lingual = True
        available_languages = ["pt", "en", "es", "fr", "de"]  # Common languages
    
    print(f"🔍 Model analysis (application method):")
    print(f"   Model: {model_name}")
    print(f"   Multi-speaker: {is_multi_speaker}")
    print(f"   Available speakers: {available_speakers[:3] if available_speakers else 'None'}")
    print(f"   Multi-lingual: {is_multi_lingual}")
    print(f"   Available languages: {available_languages[:5] if available_languages else 'None'}")
    
    # Test synthesis the same way as in the application
    print("\n🔄 Testing synthesis with application method...")
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        # Prepare synthesis parameters (same as in application)
        synthesis_params = {
            "text": "Olá, este é um teste de voz.",
            "file_path": temp_path
        }
        
        # Add speaker if model is multi-speaker (same as in application)
        if is_multi_speaker and available_speakers:
            speaker = available_speakers[0]
            synthesis_params["speaker"] = speaker
            print(f"🎤 Using speaker: {speaker}")
        elif is_multi_speaker:
            # For models like YourTTS and XTTS that need speaker_wav or speaker embedding
            print("🎤 Multi-speaker model detected but no speakers list available")
            
            # For XTTS v2, provide a default speaker
            if "xtts" in model_name.lower():
                synthesis_params["speaker"] = "default"  # XTTS v2 has a default speaker
                print("🎤 Using default speaker for XTTS v2")
            # For YourTTS, try to find a default speaker
            elif "your_tts" in model_name.lower():
                print("🎤 YourTTS detected")
        
        # Add language only if model supports it (same as in application)
        if is_multi_lingual:
            synthesis_params["language"] = "pt"
            print(f"🌍 Using language: pt")
        
        print(f"🔊 Synthesis parameters: {list(synthesis_params.keys())}")
        
        # Try synthesis
        tts.tts_to_file(**synthesis_params)
        
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            print("✅ Synthesis works with application method")
            os.unlink(temp_path)
        else:
            print("❌ Synthesis failed with application method")
    except Exception as e:
        print(f"❌ Synthesis failed with application method: {e}")
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    print("\n✅ Application method test completed")
    
except Exception as e:
    print(f"❌ Failed to test application method: {e}")
    import traceback
    traceback.print_exc()