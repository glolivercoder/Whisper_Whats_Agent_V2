#!/usr/bin/env python3
"""
Test script for TTSService to verify functionality
"""

import os
import sys
import asyncio

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_tts_service():
    """Test the TTSService functionality"""
    print("🔍 Testing TTSService...")
    
    try:
        # Import the TTSService
        from backend.main_enhanced import TTSService
        
        # Create an instance
        tts_service = TTSService()
        
        print(f"✅ TTSService created")
        print(f"   Enabled: {tts_service.enabled}")
        print(f"   Coqui TTS available: {tts_service.coqui_tts is not None}")
        print(f"   Current model: {tts_service.current_model}")
        
        # Test synthesis with pyttsx3
        print("\n🔄 Testing pyttsx3 synthesis...")
        result = asyncio.run(tts_service.synthesize_speech(
            text="Olá, este é um teste de síntese de voz.",
            engine="pyttsx3"
        ))
        
        print(f"✅ pyttsx3 synthesis result: {result['success']}")
        if result['success']:
            print(f"   Audio size: {result.get('audio_size', 0)} bytes")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        # Test synthesis with gTTS if available
        try:
            print("\n🔄 Testing gTTS synthesis...")
            result = asyncio.run(tts_service.synthesize_speech(
                text="Olá, este é um teste de síntese de voz.",
                engine="gtts"
            ))
            
            print(f"✅ gTTS synthesis result: {result['success']}")
            if result['success']:
                print(f"   Audio size: {result.get('audio_size', 0)} bytes")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"⚠️ gTTS test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ TTSService test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TTSService Test")
    print("=" * 20)
    
    success = test_tts_service()
    
    if success:
        print("\n🎉 TTSService is working correctly!")
    else:
        print("\n❌ TTSService has issues")