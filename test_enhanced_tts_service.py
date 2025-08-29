#!/usr/bin/env python3
"""
Test script for enhanced TTS service improvements
"""
import asyncio
import sys
import os
import logging

# Add backend directory to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Basic logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_tts_service_enhancements():
    """Test the enhanced TTS service with multiple scenarios"""
    print("🎵 Testing Enhanced TTS Service...")

    try:
        # Import after path setup
        from main_enhanced import tts_service

        print("✅ TTS Service imported successfully")

        # Test 1: Language code mapping
        print("\n📋 Test 1: Language Code Mapping")
        test_models = [
            'tts_models/multilingual/multi-dataset/xtts_v2',
            'tts_models/multilingual/multi-dataset/your_tts',
            'tts_models/en/ljspeech/tacotron2-DDC',
            'tts_models/es/mai/tacotron2-DDC',
            'tts_models/fr/mai/tacotron2-DDC',
            'tts_models/unknown/model',
        ]

        for model in test_models:
            lang_code = tts_service._get_language_code(model)
            print(f"  {model} → {lang_code}")

        # Test 2: Default speaker creation
        print("\n🎤 Test 2: Default Speaker Creation")
        speaker_path = os.path.join(tts_service.reference_audios_path, "default_speaker.wav")
        if os.path.exists(speaker_path):
            print(f"  ✅ Default speaker exists: {speaker_path}")
            print(f"  📊 File size: {os.path.getsize(speaker_path)} bytes")
        else:
            print("  ❌ Default speaker not found")

        # Test 3: Profile loading
        print("\n👥 Test 3: Voice Profiles")
        profiles = tts_service.get_profiles()
        print(f"  📊 Loaded {len(profiles)} voice profiles")
        for profile in profiles[:3]:  # Show first 3
            print(f"  - {profile.get('nome', 'Unnamed')} ({profile.get('modelo', 'Unknown model')})")

        # Test 4: TTS Generation (if TTS library available)
        print("\n🎵 Test 4: TTS Generation (CoquiTTS)")
        try:
            test_text = "Olá! Este é um teste do sistema TTS aprimorado."
            print(f"  📝 Test text: '{test_text[:50]}...'")

            result = await tts_service.generate_speech(
                text=test_text,
                language='tts_models/multilingual/multi-dataset/xtts_v2',  # Test multi-speaker
                format='wav',
                device='cpu'
            )

            if result['success']:
                print(f"  ✅ TTS generation successful!")
                print(f"  📁 Output: {result['filename']}")
                print(f"  🔗 URL: {result['url']}")
                print(f"  🎭 Model: {result['model_used']}")
            else:
                print(f"  ❌ TTS generation failed: {result.get('error', 'Unknown error')}")

        except ImportError as e:
            print(f"  ❌ TTS library not available: {e}")
            print("  💡 Run 'pip install TTS scipy' to enable TTS testing")
        except Exception as e:
            print(f"  ❌ TTS test failed: {e}")

        print("\n🎉 TTS Service enhancement tests completed!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tts_service_enhancements())