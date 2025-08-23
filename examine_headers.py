#!/usr/bin/env python3
"""
Examine file headers to determine actual audio format from browser
"""

import os

def examine_file_headers():
    """Examine file headers to determine format"""
    print("🔍 Examining audio file headers...")
    print("=" * 50)
    
    temp_dir = "backend/temp_audio"
    audio_files = [f for f in os.listdir(temp_dir) if f.endswith('.wav')]
    
    if not audio_files:
        print("❌ No files found")
        return
    
    # Examine first file
    file_path = os.path.join(temp_dir, audio_files[0])
    print(f"📁 Examining: {audio_files[0]}")
    
    with open(file_path, 'rb') as f:
        header = f.read(32)
    
    print(f"📊 File size: {os.path.getsize(file_path)} bytes")
    print(f"🔢 Header (first 32 bytes):")
    print(f"   Hex: {header.hex()}")
    print(f"   ASCII: {header.decode('ascii', errors='replace')}")
    
    # Check for known formats
    if header.startswith(b'RIFF'):
        print("✅ Format: WAV (RIFF)")
    elif header.startswith(b'OggS'):
        print("✅ Format: OGG")
    elif header.startswith(b'\\x1a\\x45\\xdf\\xa3'):
        print("✅ Format: WebM")
    elif header.startswith(b'fLaC'):
        print("✅ Format: FLAC")
    elif header.startswith(b'ID3') or header[0:2] == b'\\xff\\xfb':
        print("✅ Format: MP3")
    else:
        print("❓ Format: Unknown")
        print(f"   First 4 bytes: {header[:4]}")
        print(f"   Possible WebM or other format")

if __name__ == "__main__":
    examine_file_headers()