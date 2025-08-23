#!/usr/bin/env python3
"""
Test script using one of the orphaned audio files to reproduce the exact error
"""

import requests
import os

def test_with_orphaned_file():
    """Test STT with an actual orphaned file from temp_audio"""
    print("🔍 Testing with orphaned audio file...")
    
    # Use one of the orphaned files
    audio_file_path = "backend/temp_audio/original_1755929935365.wav"
    
    if not os.path.exists(audio_file_path):
        print(f"❌ File not found: {audio_file_path}")
        return
    
    print(f"📁 Using file: {audio_file_path}")
    print(f"📊 File size: {os.path.getsize(audio_file_path)} bytes")
    
    try:
        # Read the file and send to STT endpoint
        with open(audio_file_path, 'rb') as f:
            audio_data = f.read()
        
        url = "http://localhost:8001/api/stt"
        files = {
            'audio': ('test_audio.wav', audio_data, 'audio/wav')
        }
        
        print(f"📤 Sending request to {url}...")
        response = requests.post(url, files=files, timeout=30)
        
        print(f"📋 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📝 Transcription: '{result.get('text', 'N/A')}'")
        else:
            print("❌ FAILED!")
            print(f"Error details: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🤖 Testing STT with orphaned audio file")
    print("=" * 50)
    test_with_orphaned_file()