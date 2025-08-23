#!/usr/bin/env python3
"""
Analyze audio file format to understand transcription issues
"""

import os
import wave
import librosa
import soundfile as sf
import numpy as np

def analyze_audio_file(file_path):
    """Analyze audio file format and content"""
    print(f"🔍 Analyzing audio file: {file_path}")
    print("=" * 60)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    file_size = os.path.getsize(file_path)
    print(f"📊 File size: {file_size} bytes")
    
    # Try to analyze with wave module
    try:
        with wave.open(file_path, 'rb') as wav_file:
            print("🎵 WAV file analysis:")
            print(f"   Channels: {wav_file.getnchannels()}")
            print(f"   Sample width: {wav_file.getsampwidth()} bytes")
            print(f"   Frame rate: {wav_file.getframerate()} Hz")
            print(f"   Frames: {wav_file.getnframes()}")
            print(f"   Duration: {wav_file.getnframes() / wav_file.getframerate():.2f} seconds")
    except Exception as e:
        print(f"❌ WAV analysis failed: {e}")
    
    # Try to read with librosa
    try:
        print("\\n🔊 Librosa analysis:")
        audio_data, sr = librosa.load(file_path, sr=None)
        print(f"   Sample rate: {sr} Hz")
        print(f"   Audio shape: {audio_data.shape}")
        print(f"   Duration: {len(audio_data) / sr:.2f} seconds")
        print(f"   Min value: {np.min(audio_data):.6f}")
        print(f"   Max value: {np.max(audio_data):.6f}")
        print(f"   RMS: {np.sqrt(np.mean(audio_data**2)):.6f}")
        
        # Check if audio is silent
        if np.max(np.abs(audio_data)) < 0.001:
            print("⚠️ Audio appears to be silent or very quiet!")
            
    except Exception as e:
        print(f"❌ Librosa analysis failed: {e}")
    
    # Try to read with soundfile
    try:
        print("\\n📁 SoundFile analysis:")
        info = sf.info(file_path)
        print(f"   Format: {info.format}")
        print(f"   Subtype: {info.subtype}")
        print(f"   Endian: {info.endian}")
        print(f"   Channels: {info.channels}")
        print(f"   Frames: {info.frames}")
        print(f"   Sample rate: {info.samplerate} Hz")
        print(f"   Duration: {info.duration:.2f} seconds")
        
        # Read a small sample
        data, samplerate = sf.read(file_path, frames=1000)
        print(f"   Sample data shape: {data.shape}")
        print(f"   Sample data type: {data.dtype}")
        
    except Exception as e:
        print(f"❌ SoundFile analysis failed: {e}")

def main():
    """Analyze multiple orphaned files"""
    print("🤖 Audio File Format Analysis")
    print("=" * 60)
    
    temp_dir = "backend/temp_audio"
    if not os.path.exists(temp_dir):
        print(f"❌ Directory not found: {temp_dir}")
        return
    
    # Find audio files
    audio_files = [f for f in os.listdir(temp_dir) if f.endswith('.wav')]
    
    if not audio_files:
        print(f"❌ No audio files found in {temp_dir}")
        return
    
    print(f"📁 Found {len(audio_files)} audio files")
    
    # Analyze first few files
    for i, filename in enumerate(audio_files[:3]):
        file_path = os.path.join(temp_dir, filename)
        print(f"\\n📋 File {i+1}: {filename}")
        analyze_audio_file(file_path)

if __name__ == "__main__":
    main()