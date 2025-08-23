#!/usr/bin/env python3
"""
Debug script to test STT endpoint directly and see detailed logs
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

def test_stt_with_debug():
    """Test the STT endpoint with enhanced debugging"""
    print("🧪 Testing STT Endpoint with Enhanced Logging")
    print("=" * 60)
    
    try:
        # Create test audio
        print("🎵 Creating test audio file...")
        audio_data = create_test_audio()
        print(f"📊 Audio size: {len(audio_data)} bytes")
        
        # Test server health first
        print("🔍 Testing server health...")
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"   Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Whisper Loaded: {health_data.get('whisper_loaded')}")
            print(f"   Version: {health_data.get('version')}")
        
        # Prepare the STT request
        url = "http://localhost:8001/api/stt"
        files = {
            'audio': ('debug_test.wav', audio_data, 'audio/wav')
        }
        
        print(f"\n📤 Sending STT request to {url}...")
        print(f"   Content-Type: audio/wav")
        print(f"   File size: {len(audio_data)} bytes")
        
        start_time = time.time()
        
        # Make the request with detailed error handling
        try:
            response = requests.post(url, files=files, timeout=60)
            elapsed_time = time.time() - start_time
            
            print(f"\n📋 Response received in {elapsed_time:.2f}s")
            print(f"   Status Code: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ STT Request SUCCESSFUL!")
                print(f"   Request ID: {result.get('request_id', 'N/A')}")
                print(f"   Transcription: '{result.get('text', 'N/A')}'")
                print(f"   Method Used: {result.get('transcription_method', 'N/A')}")
                print(f"   Processing Time: {result.get('processing_time', 'N/A')}s")
                print(f"   Confidence: {result.get('confidence', 'N/A')}")
                return True
            else:
                print(f"\n❌ STT Request FAILED!")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("\n⏱️ Request timed out (>60s)")
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"\n🔌 Connection error: {e}")
            return False
        except Exception as e:
            print(f"\n💥 Request error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Test setup error: {e}")
        return False

def main():
    """Run the debug test"""
    print("🤖 STT Endpoint Debug Test")
    print("=" * 60)
    
    success = test_stt_with_debug()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 DEBUG TEST PASSED!")
        print("✅ STT endpoint is working correctly")
        print("📋 Check server logs for detailed processing info")
    else:
        print("⚠️ DEBUG TEST FAILED!")
        print("📋 Check both server logs and error messages above")
    
    print("\n📂 Log Files to Check:")
    print("   • Server Terminal: Real-time logs")
    print("   • logs/stt_debug.log: Detailed file logs")
    print("   • Browser DevTools: Frontend errors")

if __name__ == "__main__":
    main()