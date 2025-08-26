#!/usr/bin/env python3
"""
Test script to verify Coqui TTS fixes work correctly
"""

import os
import sys
import warnings

def apply_mecab_fixes():
    """Apply MeCab fixes before any TTS imports"""
    print("🔧 Applying MeCab fixes...")
    
    # Set environment variables to bypass MeCab issues on Windows
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Try to create a dummy mecabrc file
    try:
        import tempfile
        temp_dir = tempfile.gettempdir()
        mecabrc_path = os.path.join(temp_dir, 'mecabrc')
        if not os.path.exists(mecabrc_path):
            with open(mecabrc_path, 'w') as f:
                f.write("# Dummy mecabrc file to prevent MeCab errors\n")
            print(f"✅ Created dummy mecabrc at {mecabrc_path}")
    except Exception as e:
        print(f"⚠️ Could not create dummy mecabrc: {e}")
        
    # Suppress MeCab warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    print("✅ MeCab fixes applied")

def test_tts_import():
    """Test if we can import TTS without MeCab errors"""
    print("🧪 Testing TTS import...")
    
    try:
        from TTS.api import TTS
        print("✅ TTS imported successfully")
        return True
    except Exception as e:
        print(f"❌ TTS import failed: {e}")
        return False

def test_model_loading():
    """Test loading different models"""
    print("🧪 Testing model loading...")
    
    models_to_test = [
        "tts_models/multilingual/multi-dataset/xtts_v2",
        "tts_models/multilingual/multi-dataset/your_tts",
        "tts_models/pt/cv/vits"
    ]
    
    successful_models = []
    
    for model_name in models_to_test:
        try:
            print(f"  Testing {model_name}...")
            from TTS.api import TTS  # Import inside loop to ensure it's available
            tts_instance = TTS(model_name=model_name, progress_bar=False, gpu=False)
            print(f"  ✅ {model_name} loaded successfully")
            successful_models.append(model_name)
        except Exception as e:
            print(f"  ❌ {model_name} failed: {str(e)[:100]}...")
    
    return successful_models

def main():
    """Main test function"""
    print("🚀 Coqui TTS Fix Verification")
    print("=" * 40)
    
    # Apply fixes
    apply_mecab_fixes()
    
    # Test import
    if not test_tts_import():
        print("❌ TTS import test failed")
        return False
    
    # Test model loading
    successful_models = test_model_loading()
    
    if successful_models:
        print(f"\n🎉 Success! Loaded models: {successful_models}")
        print("✅ Coqui TTS fixes are working correctly!")
        return True
    else:
        print("\n❌ No models loaded successfully")
        print("⚠️ Coqui TTS may still have issues")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)