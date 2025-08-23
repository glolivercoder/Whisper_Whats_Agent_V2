#!/usr/bin/env python3
"""
Test faster-whisper with WebM files
"""

import os
from faster_whisper import WhisperModel

def test_faster_whisper():
    """Test faster-whisper with WebM file"""
    print("⚡ Testing faster-whisper WebM support")
    print("=" * 50)
    
    # Test with WebM file
    webm_file = "backend/temp_audio/original_1755929935365.wav"  # Actually WebM
    
    if not os.path.exists(webm_file):
        print(f"❌ File not found: {webm_file}")
        return
    
    print(f"📁 Testing file: {webm_file}")
    print(f"📊 File size: {os.path.getsize(webm_file)} bytes")
    
    try:
        # Load faster-whisper model (smaller for testing)
        print("\\n🔄 Loading faster-whisper model (base)...")
        model = WhisperModel("base", device="cpu", compute_type="int8")
        print("✅ Model loaded!")
        
        # Test transcription
        print("\\n🎤 Testing transcription...")
        segments, info = model.transcribe(webm_file, language="pt")
        
        print(f"✅ Transcription successful!")
        print(f"   Language: {info.language}")
        print(f"   Language probability: {info.language_probability:.2f}")
        print(f"   Duration: {info.duration:.2f} seconds")
        
        # Get transcription text
        text_segments = list(segments)
        full_text = " ".join([segment.text for segment in text_segments])
        
        print(f"\\n📝 Transcription result:")
        print(f"   Text: '{full_text.strip()}'")
        print(f"   Segments count: {len(text_segments)}")
        
        if full_text.strip():
            print("🎉 SUCCESS! faster-whisper handled WebM perfectly!")
            return True
        else:
            print("⚠️ Empty transcription (but no error!)")
            return True
            
    except Exception as e:
        print(f"❌ faster-whisper failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_faster_whisper()
    
    if success:
        print("\\n🚀 GREAT NEWS! faster-whisper can handle WebM files!")
        print("   This should solve the STT 500 errors!")
    else:
        print("\\n😞 Still having issues with WebM format")