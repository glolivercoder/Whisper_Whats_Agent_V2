#!/usr/bin/env python3
"""
Simple script to apply Coqui TTS fixes
"""

import os
import tempfile
import warnings

def apply_fixes():
    """Apply all necessary fixes for Coqui TTS"""
    print("🔧 Applying Coqui TTS fixes...")
    
    # Set environment variables
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Create dummy mecabrc file
    try:
        temp_dir = tempfile.gettempdir()
        mecabrc_path = os.path.join(temp_dir, 'mecabrc')
        
        if not os.path.exists(mecabrc_path):
            with open(mecabrc_path, 'w') as f:
                f.write("# Dummy mecabrc file to prevent MeCab errors\n")
            print(f"✅ Created dummy mecabrc at {mecabrc_path}")
    except Exception as e:
        print(f"⚠️ Could not create dummy mecabrc: {e}")
    
    # Suppress warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    print("✅ All fixes applied!")

if __name__ == "__main__":
    apply_fixes()
    print("🔧 Coqui TTS fixes applied successfully!")