#!/usr/bin/env python3
"""
Create a simple test audio file for XTTS v2 voice cloning testing
"""

import numpy as np
import wave
import struct

def create_test_audio(filename="test_reference.wav", duration=10, sample_rate=22050):
    """Create a simple test audio file with a sine wave tone"""
    # Generate a simple sine wave at 440 Hz (A4 note)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * 440 * t)
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"✅ Created test audio file: {filename} ({duration} seconds)")

if __name__ == "__main__":
    create_test_audio()