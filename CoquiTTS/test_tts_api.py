#!/usr/bin/env python3
"""
Test script for TTS API functionality
"""

import requests
import json
import base64
import os

def test_tts_api():
    """Test the TTS API endpoint"""
    url = "http://localhost:8001/api/tts"
    
    # Test data
    data = {
        "text": "Olá, este é um teste de síntese de voz com Coqui TTS funcionando corretamente.",
        "engine": "coqui",
        "language": "pt-BR"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Testing TTS API...")
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ TTS API test successful!")
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            print(f"Audio size: {result.get('audio_size', 0)} bytes")
            
            # Save audio file if available
            if result.get('audio_data'):
                audio_data = base64.b64decode(result['audio_data'])
                with open("test_tts_output.wav", "wb") as f:
                    f.write(audio_data)
                print("💾 Audio saved as test_tts_output.wav")
            
            return True
        else:
            print(f"❌ TTS API test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TTS API: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TTS API Test")
    print("=" * 30)
    
    if test_tts_api():
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Some tests failed!")