#!/usr/bin/env python3
"""
Test script for STT endpoint with actual audio file
"""

import requests
import wave
import numpy as np
import io
import time

def create_test_audio():
    """Create a simple test audio file"""
    # Generate a simple sine wave for testing
    sample_rate = 16000
    duration = 2.0  # seconds
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create WAV file in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    wav_buffer.seek(0)
    return wav_buffer.getvalue()

def test_stt_endpoint():
    """Test the STT endpoint"""
    print("🧪 Testing STT Endpoint...")
    
    try:
        # Create test audio
        print("🎵 Creating test audio file...")
        audio_data = create_test_audio()
        print(f"📊 Audio size: {len(audio_data)} bytes")
        
        # Prepare the request
        url = "http://localhost:8001/api/stt"
        files = {
            'audio': ('test_audio.wav', audio_data, 'audio/wav')
        }
        
        print(f"📤 Sending request to {url}...")
        start_time = time.time()
        
        response = requests.post(url, files=files, timeout=30)
        
        elapsed_time = time.time() - start_time
        
        print(f"⏱️ Request completed in {elapsed_time:.2f}s")
        print(f"📋 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ STT Test SUCCESSFUL!")
            print(f"📝 Transcription: '{result.get('text', 'N/A')}'")
            print(f"🕐 Processing Time: {result.get('processing_time', 'N/A')}s")
            print(f"📈 Confidence: {result.get('confidence', 'N/A')}")
            return True
        else:
            print(f"❌ STT Test FAILED!")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing Health Endpoint...")
    
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check PASSED!")
            print(f"📊 Status: {data.get('status')}")
            print(f"🧠 Whisper Loaded: {data.get('whisper_loaded')}")
            print(f"🏷️ Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Health Check FAILED! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 WhatsApp Voice Agent V2 - STT Test Suite")
    print("=" * 50)
    
    # Test health first
    health_ok = test_health_endpoint()
    print()
    
    if health_ok:
        # Test STT endpoint
        stt_ok = test_stt_endpoint()
        print()
        
        if stt_ok:
            print("🎉 ALL TESTS PASSED!")
            print("✅ STT endpoint is working correctly")
            print("🎯 Ready for voice transcription!")
        else:
            print("⚠️ STT test failed - check server logs")
    else:
        print("❌ Server not healthy - check if it's running")
    
    print("\n📋 Next Steps:")
    print("1. Open browser: http://localhost:8001")
    print("2. Test voice recording interface")
    print("3. Check Manual.html for complete guide")

if __name__ == "__main__":
    main()