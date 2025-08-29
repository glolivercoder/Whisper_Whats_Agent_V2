#!/usr/bin/env python3
"""
🔊 CRIATE DEFAULT SPEAKER WAV

Esta script cria um arquivo WAV simples de referência
para modelos multi-speaker que precisam de referência de voz.
"""

import numpy as np
from scipy.io.wavfile import write
import os

def create_default_speaker_wav(output_path="./reference_audios/default_speaker.wav", sample_rate=22050, duration=2.0):
    """Cria um arquivo WAV simples para referência de voz"""

    # Create a simple audio signal (sine wave + noise simulation)
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Simulate a simple voice-like sound
    frequency = 220  # A3 note (typical male voice range)
    audio = np.sin(frequency * 2 * np.pi * t)

    # Add some noise to make it more voice-like
    noise = np.random.normal(0, 0.1, len(audio))
    audio = audio + noise

    # Normalize
    audio = audio / np.max(np.abs(audio))

    # Convert to 16-bit WAV format
    audio_int16 = (audio * 32767).astype(np.int16)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write WAV file
    write(output_path, sample_rate, audio_int16)

    print(f"✅ Default speaker WAV created: {output_path}")
    print(f"   Duration: {duration}s")
    print(f"   Sample rate: {sample_rate}Hz")

def main():
    """Main function"""
    import os

    print("🔊 Creating Default Speaker WAV")
    print("=" * 40)

    output_path = "./reference_audios/default_speaker.wav"

    try:
        create_default_speaker_wav(output_path)
        print("\n✅ Default speaker WAV created successfully!")
        print(f"📍 Location: {os.path.abspath(output_path)}")
        print("\n💡 Usage:")
        print("   - Used as fallback reference for multi-speaker models")
        print("   - XTTS v2 will use this when no custom voice is provided")

    except Exception as e:
        print(f"❌ Error creating default speaker WAV: {e}")

    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()