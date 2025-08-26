#!/usr/bin/env python3
"""
Test the complete voice cloning workflow as implemented in the TTSService
"""

import os
import sys
import json
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

class MockTTSService:
    """Mock TTSService to test the voice cloning workflow"""
    
    def __init__(self):
        self.coqui_tts = None
        self.current_model = None
        self.load_xtts_v2_model()
    
    def load_xtts_v2_model(self):
        """Load XTTS v2 model"""
        try:
            import TTS.api
            print("🔄 Loading XTTS v2 model...")
            self.coqui_tts = TTS.api.TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=False,
                gpu=False
            )
            self.current_model = "tts_models/multilingual/multi-dataset/xtts_v2"
            print("✅ XTTS v2 model loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to load XTTS v2 model: {e}")
            return False
    
    async def synthesize_speech(self, text: str, voice: str = "", 
                               speed: float = 1.0, language: str = "", engine: str = ""):
        """Synthesize speech with voice cloning support - simplified version of the actual method"""
        try:
            # Check if this is a cloned voice request
            is_cloned_voice = voice and (voice.startswith('cloned_') or voice.startswith('cloned:'))
            cloned_voice_name = ""
            
            if is_cloned_voice:
                # Handle both formats of cloned voice naming
                if voice.startswith('cloned:'):
                    cloned_voice_name = voice.replace('cloned:', '')
                else:
                    cloned_voice_name = voice.replace('cloned_', '')
                print(f"🎭 TTS: Using cloned voice '{cloned_voice_name}' for '{text[:50]}...'")
            else:
                print(f"🔊 TTS: Synthesizing '{text[:50]}...' with voice {voice}")
            
            # Use Coqui TTS to generate audio
            if self.coqui_tts:
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                temp_path = temp_file.name
                temp_file.close()
                
                if is_cloned_voice:
                    # For cloned voices, check for reference audio
                    print(f"🎤 Using advanced model with speaker embedding for cloned voice '{cloned_voice_name}'")
                    
                    # Check if we have a reference audio file for this cloned voice
                    ref_audio_dir = os.path.join(os.getcwd(), "reference_audio")
                    ref_audio_path = None
                    
                    if os.path.exists(ref_audio_dir):
                        # Look for reference audio files matching the cloned voice name
                        for filename in os.listdir(ref_audio_dir):
                            if cloned_voice_name.lower() in filename.lower() and filename.endswith(('.wav', '.mp3', '.flac')):
                                ref_audio_path = os.path.join(ref_audio_dir, filename)
                                break
                    
                    # Also check for the test reference audio
                    if not ref_audio_path and os.path.exists("test_reference.wav"):
                        ref_audio_path = "test_reference.wav"
                        print(f"🎵 Using test reference audio: {ref_audio_path}")
                    
                    # XTTS v2 supports speaker_wav parameter for voice cloning
                    if ref_audio_path and os.path.exists(ref_audio_path):
                        print(f"🎵 Using reference audio: {ref_audio_path}")
                        # Use the reference audio for voice cloning with speaker_wav parameter
                        self.coqui_tts.tts_to_file(
                            text=text,
                            file_path=temp_path,
                            speaker_wav=ref_audio_path,
                            language="pt"  # Portuguese
                        )
                    else:
                        print(f"⚠️ No reference audio found for cloned voice '{cloned_voice_name}', using default speaker")
                        # Fallback to default speaker
                        self.coqui_tts.tts_to_file(text=text, file_path=temp_path, language="pt")
                else:
                    # Regular synthesis
                    language_code = "pt" if "pt" in (language or "").lower() else "en"
                    self.coqui_tts.tts_to_file(text=text, file_path=temp_path, language=language_code)
                
                # Read audio data
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()
                
                # Cleanup
                os.unlink(temp_path)
                
                print(f"✅ Speech synthesis completed, audio size: {len(audio_data)} bytes")
                
                return {
                    "success": True,
                    "message": f"TTS generated with {'cloned voice' if is_cloned_voice else 'Coqui TTS'}",
                    "audio_size": len(audio_data),
                    "method": f"coqui_tts_cloned_{cloned_voice_name}" if is_cloned_voice else f"coqui_tts_{self.current_model}"
                }
            else:
                return {"success": False, "error": "Coqui TTS not available"}
                
        except Exception as coqui_error:
            print(f"❌ Coqui TTS failed: {coqui_error}")
            return {"success": False, "error": f"Coqui TTS failed: {str(coqui_error)}"}

async def test_voice_cloning_workflow():
    """Test the complete voice cloning workflow"""
    print("🧪 Testing complete voice cloning workflow...")
    
    # Create mock TTS service
    tts_service = MockTTSService()
    
    if not tts_service.coqui_tts:
        print("❌ Failed to initialize TTS service")
        return
    
    # Test 1: Regular voice synthesis
    print("\n--- Test 1: Regular voice synthesis ---")
    result = await tts_service.synthesize_speech(
        text="Olá, esta é uma mensagem de teste.",
        voice="pt-BR-Wavenet-A",
        language="pt-BR"
    )
    print(f"Result: {result}")
    
    # Test 2: Cloned voice synthesis (without reference audio)
    print("\n--- Test 2: Cloned voice synthesis (without reference audio) ---")
    result = await tts_service.synthesize_speech(
        text="Olá, esta é uma voz clonada.",
        voice="cloned_test_voice",
        language="pt-BR"
    )
    print(f"Result: {result}")
    
    # Test 3: Create a reference audio directory and test with reference audio
    print("\n--- Test 3: Cloned voice synthesis (with reference audio) ---")
    
    # Create reference_audio directory
    ref_audio_dir = os.path.join(os.getcwd(), "reference_audio")
    os.makedirs(ref_audio_dir, exist_ok=True)
    
    # Copy test reference audio to reference_audio directory
    import shutil
    if os.path.exists("test_reference.wav"):
        shutil.copy("test_reference.wav", os.path.join(ref_audio_dir, "test_voice.wav"))
        print("📁 Copied test reference audio to reference_audio directory")
    
    result = await tts_service.synthesize_speech(
        text="Olá, esta é uma voz clonada com referência de áudio.",
        voice="cloned_test_voice",
        language="pt-BR"
    )
    print(f"Result: {result}")
    
    print("\n✅ Voice cloning workflow test completed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_voice_cloning_workflow())