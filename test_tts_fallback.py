#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for TTS fallback functionality
Tests if TTS works when Coqui is not available
"""

import requests
import json
import time

def test_tts_fallback():
    """Test TTS with different engines when Coqui TTS is not available"""
    base_url = "http://localhost:8001"
    
    print("🧪 Testing TTS Fallback Functionality")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. 🔍 Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health = response.json()
            tts_status = health.get("services", {}).get("tts_service", {})
            print(f"   ✅ Health check passed")
            print(f"   📊 TTS Status: {tts_status.get('status')}")
            print(f"   🔊 Coqui Loaded: {tts_status.get('coqui_loaded')}")
            print(f"   🔄 Fallback Available: {tts_status.get('fallback_available')}")
            print(f"   🌍 Language: {tts_status.get('language')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: TTS Models endpoint
    print("\n2. 📋 Testing TTS Models endpoint...")
    try:
        response = requests.get(f"{base_url}/api/tts/models", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"   ✅ Models endpoint working")
            print(f"   📊 Available models: {models.get('total_models', 0)}")
            print(f"   🎯 Default model: {models.get('default_model')}")
        else:
            print(f"   ❌ Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Models endpoint error: {e}")
    
    # Test 3: TTS with Coqui engine (should fallback)
    print("\n3. 🔊 Testing TTS with Coqui engine (should fallback)...")
    try:
        tts_request = {
            "text": "Olá, este é um teste da síntese de voz em português",
            "engine": "coqui",
            "voice": "tts_models/pt/cv/vits",
            "language": "pt-BR"
        }
        
        response = requests.post(
            f"{base_url}/api/tts", 
            json=tts_request, 
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ TTS request successful")
            print(f"   🎭 Method used: {result.get('method', 'unknown')}")
            print(f"   📝 Message: {result.get('message')}")
            print(f"   📊 Audio size: {result.get('audio_size', 0)} bytes")
            print(f"   🎵 Has audio data: {'Yes' if result.get('audio_data') else 'No'}")
        else:
            print(f"   ❌ TTS request failed: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ TTS request error: {e}")
    
    # Test 4: TTS with pyttsx3 engine directly
    print("\n4. 🎤 Testing TTS with pyttsx3 engine directly...")
    try:
        tts_request = {
            "text": "Teste direto do pyttsx3",
            "engine": "pyttsx3",
            "language": "pt-BR"
        }
        
        response = requests.post(
            f"{base_url}/api/tts", 
            json=tts_request, 
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ pyttsx3 TTS successful")
            print(f"   🎭 Method used: {result.get('method', 'unknown')}")
            print(f"   📊 Audio size: {result.get('audio_size', 0)} bytes")
        else:
            print(f"   ❌ pyttsx3 TTS failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ pyttsx3 TTS error: {e}")
    
    # Test 5: TTS with gTTS engine
    print("\n5. 🌐 Testing TTS with gTTS engine...")
    try:
        tts_request = {
            "text": "Teste com Google TTS online",
            "engine": "gtts",
            "language": "pt-BR"
        }
        
        response = requests.post(
            f"{base_url}/api/tts", 
            json=tts_request, 
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ gTTS successful")
            print(f"   🎭 Method used: {result.get('method', 'unknown')}")
            print(f"   📊 Audio size: {result.get('audio_size', 0)} bytes")
        else:
            print(f"   ❌ gTTS failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ gTTS error: {e}")
    
    print("\n🎉 TTS Fallback Test Completed!")
    print("🔍 Check the server logs to see the fallback behavior in action.")
    return True

if __name__ == "__main__":
    test_tts_fallback()