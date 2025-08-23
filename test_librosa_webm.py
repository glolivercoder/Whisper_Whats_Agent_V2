#!/usr/bin/env python3
"""
Test librosa directly with WebM files
"""

import os
import librosa
import numpy as np

def test_librosa_webm():
    """Test librosa with WebM file directly"""
    print("🔊 Testing librosa WebM support")
    print("=" * 50)
    
    # Test with one of the orphaned WebM files
    webm_file = "backend/temp_audio/original_1755929935365.wav"  # Actually WebM format
    
    if not os.path.exists(webm_file):
        print(f"❌ File not found: {webm_file}")
        return
    
    print(f"📁 Testing file: {webm_file}")
    print(f"📊 File size: {os.path.getsize(webm_file)} bytes")
    
    try:
        # Test basic librosa load
        print("\\n🔄 Testing librosa.load()...")
        audio_data, sr = librosa.load(webm_file, sr=16000)
        
        print(f"✅ Success!")
        print(f"   Audio shape: {audio_data.shape}")
        print(f"   Sample rate: {sr}")
        print(f"   Duration: {len(audio_data) / sr:.2f} seconds")
        print(f"   Min/Max values: {np.min(audio_data):.6f} / {np.max(audio_data):.6f}")
        print(f"   RMS level: {np.sqrt(np.mean(audio_data**2)):.6f}")
        
        if len(audio_data) > 0:
            print(f"✅ Audio data loaded successfully!")
        else:
            print(f"⚠️ Audio data is empty")
            
    except Exception as e:
        print(f"❌ Librosa failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Try with different parameters
        try:
            print("\\n🔄 Trying with sr=None...")
            audio_data, sr = librosa.load(webm_file, sr=None)
            print(f"✅ Success with sr=None: shape={audio_data.shape}, sr={sr}")
        except Exception as e2:
            print(f"❌ Also failed with sr=None: {e2}")

if __name__ == "__main__":
    test_librosa_webm()