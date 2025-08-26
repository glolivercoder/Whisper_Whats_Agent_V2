#!/usr/bin/env python3
"""
Simple test script to verify MeCab fixes work
"""

import os
import sys

def apply_mecab_fixes():
    """Apply MeCab fixes"""
    print("Applying MeCab fixes...")
    
    # Set environment variables
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Create dummy mecabrc
    try:
        import tempfile
        temp_dir = tempfile.gettempdir()
        mecabrc_path = os.path.join(temp_dir, 'mecabrc')
        if not os.path.exists(mecabrc_path):
            with open(mecabrc_path, 'w') as f:
                f.write("# Dummy mecabrc\n")
        print(f"Created dummy mecabrc at {mecabrc_path}")
    except Exception as e:
        print(f"Could not create mecabrc: {e}")
    
    print("MeCab fixes applied!")

def test_import():
    """Test TTS import"""
    print("Testing TTS import...")
    try:
        from TTS.api import TTS
        print("✅ TTS imported successfully")
        return True
    except Exception as e:
        print(f"❌ TTS import failed: {e}")
        return False

def main():
    print("Testing MeCab fixes for Coqui TTS...")
    apply_mecab_fixes()
    
    if test_import():
        print("🎉 Success! Coqui TTS should work now.")
    else:
        print("❌ Still having issues with Coqui TTS.")

if __name__ == "__main__":
    main()