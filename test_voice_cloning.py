#!/usr/bin/env python3
"""
Test script for voice cloning functionality
Tests the new API endpoints for voice cloning features
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8001"

def test_tts_models():
    """Test if TTS models endpoint is working"""
    print("🔍 Testing TTS models endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/tts/models")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available models: {len(data.get('models', []))}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_train_voice_clone():
    """Test voice cloning training endpoint"""
    print("\n🎯 Testing voice clone training...")
    try:
        payload = {
            "voice_name": "test_voice_1"
        }
        response = requests.post(f"{BASE_URL}/api/tts/train-clone", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Training successful: {data.get('message')}")
            print(f"Voice: {data.get('voice_name')}")
            print(f"Training time: {data.get('training_time')}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cloned_voice():
    """Test cloned voice synthesis"""
    print("\n🔊 Testing cloned voice synthesis...")
    try:
        payload = {
            "voice_name": "test_voice_1",
            "text": "Olá, este é um teste da voz clonada em português brasileiro."
        }
        response = requests.post(f"{BASE_URL}/api/tts/test-clone", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Voice test successful: {data.get('message')}")
            print(f"Method: {data.get('method')}")
            print(f"Has audio data: {bool(data.get('audio_data'))}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_regular_tts():
    """Test regular TTS functionality"""
    print("\n🔊 Testing regular TTS...")
    try:
        payload = {
            "text": "Este é um teste do TTS regular em português brasileiro.",
            "language": "pt-BR",
            "voice": "tts_models/pt/cv/vits"
        }
        response = requests.post(f"{BASE_URL}/api/tts", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TTS successful: {data.get('message')}")
            print(f"Method: {data.get('method')}")
            print(f"Has audio data: {bool(data.get('audio_data'))}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Voice Cloning Functionality")
    print("=" * 50)
    
    tests = [
        ("TTS Models", test_tts_models),
        ("Voice Clone Training", test_train_voice_clone), 
        ("Cloned Voice Test", test_cloned_voice),
        ("Regular TTS", test_regular_tts)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("-" * 30)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All voice cloning features are working!")
    else:
        print("⚠️ Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()