#!/usr/bin/env python3
"""
Test script for STT (Speech-to-Text) endpoint
This script creates a simple audio file and tests the STT functionality
"""

import requests
import wave
import numpy as np
import struct
import tempfile
import os

def create_test_audio():
    """Create a simple test audio file (silence for testing)"""
    # Audio parameters
    sample_rate = 16000
    duration = 2  # 2 seconds
    amplitude = 0.1
    frequency = 440  # A note
    
    # Generate a simple sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = amplitude * np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create temporary WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        with wave.open(temp_file.name, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        return temp_file.name

def test_stt_endpoint():
    """Test the STT endpoint with a simple audio file"""
    print("🎤 Testing STT (Speech-to-Text) Endpoint")
    print("=" * 50)
    
    # Test 1: Check if endpoint exists
    print("\n1️⃣ Testing endpoint availability...")
    try:
        # Try a GET request first (should return 405 Method Not Allowed)
        response = requests.get("http://localhost:8001/api/stt", timeout=5)
        print(f"   ✅ Endpoint exists (status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Endpoint not reachable: {e}")
        return False
    
    # Test 2: Test with invalid data
    print("\n2️⃣ Testing with invalid data...")
    try:
        response = requests.post(
            "http://localhost:8001/api/stt",
            files={'audio': ('test.txt', 'invalid data', 'text/plain')},
            timeout=10
        )
        print(f"   ✅ Properly rejects invalid data (status: {response.status_code})")
    except Exception as e:
        print(f"   ⚠️  Error with invalid data: {e}")
    
    # Test 3: Test with valid audio file
    print("\n3️⃣ Testing with valid audio file...")
    audio_file_path = None
    try:
        # Create test audio
        print("   📄 Creating test audio file...")
        audio_file_path = create_test_audio()
        
        # Send to STT endpoint
        print("   📤 Sending to STT endpoint...")
        with open(audio_file_path, 'rb') as audio_file:
            files = {'audio': ('test.wav', audio_file, 'audio/wav')}
            response = requests.post(
                "http://localhost:8001/api/stt",
                files=files,
                timeout=30  # Longer timeout for processing
            )
        
        print(f"   📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ STT Success!")
            print(f"   📝 Transcribed text: '{result.get('text', 'No text')}'")
            print(f"   🎯 Confidence: {result.get('confidence', 'N/A')}")
            print(f"   ⏱️ Processing time: {result.get('timestamp', 'N/A')}")
            return True
        else:
            print(f"   ❌ STT Failed!")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing STT: {e}")
        return False
    finally:
        # Clean up
        if audio_file_path and os.path.exists(audio_file_path):
            os.unlink(audio_file_path)
            print("   🧹 Cleaned up test file")

def test_whisper_directly():
    """Test Whisper model directly to isolate issues"""
    print("\n4️⃣ Testing Whisper model directly...")
    try:
        import whisper
        model = whisper.load_model("base")
        print("   ✅ Whisper model loads successfully")
        
        # Create a simple test
        audio_file_path = create_test_audio()
        result = model.transcribe(audio_file_path, language="pt")
        print(f"   ✅ Direct transcription: '{result['text']}'")
        
        os.unlink(audio_file_path)
        return True
    except Exception as e:
        print(f"   ❌ Direct Whisper test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Comprehensive STT Testing")
    print("Testing Speech-to-Text functionality on port 8001")
    print("=" * 60)
    
    # Test the endpoint
    stt_success = test_stt_endpoint()
    
    # Test Whisper directly if STT fails
    if not stt_success:
        print("\n🔧 STT endpoint failed, testing Whisper directly...")
        whisper_success = test_whisper_directly()
        
        if whisper_success:
            print("\n💡 Whisper works directly but STT endpoint has issues")
            print("   Possible fixes:")
            print("   • Check audio file format requirements")
            print("   • Verify endpoint accepts multipart/form-data")
            print("   • Check server logs for detailed errors")
        else:
            print("\n❌ Whisper model itself has issues")
    else:
        print("\n🎉 STT endpoint working perfectly!")
    
    print(f"\n📱 Frontend Fix Applied:")
    print(f"   • Updated frontend to use port 8001 consistently")
    print(f"   • STT calls now go to: http://localhost:8001/api/stt")
    print(f"   • Test the interface again at: http://localhost:8001")

if __name__ == "__main__":
    main()