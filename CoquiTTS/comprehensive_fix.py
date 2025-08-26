#!/usr/bin/env python3
"""
Comprehensive fix script for Coqui TTS issues on Windows
"""

import os
import sys
import subprocess
import warnings
import tempfile

def apply_all_fixes():
    """Apply all necessary fixes for Coqui TTS on Windows"""
    print("🔧 Applying comprehensive fixes for Coqui TTS on Windows...")
    
    # 1. Set environment variables
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    print("✅ Environment variables set")
    
    # 2. Create dummy mecabrc file
    try:
        temp_dir = tempfile.gettempdir()
        mecabrc_path = os.path.join(temp_dir, 'mecabrc')
        
        if not os.path.exists(mecabrc_path):
            with open(mecabrc_path, 'w') as f:
                f.write("# Dummy mecabrc file to prevent MeCab errors\n")
            print(f"✅ Created dummy mecabrc at {mecabrc_path}")
    except Exception as e:
        print(f"⚠️ Could not create dummy mecabrc: {e}")
    
    # 3. Suppress warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    print("✅ Warning filters applied")
    
    print("✅ All fixes applied successfully")

def test_import_with_fixes():
    """Test importing TTS with all fixes applied"""
    print("🧪 Testing TTS import with fixes...")
    
    # Apply fixes first
    apply_all_fixes()
    
    # Capture stderr to suppress MeCab error messages
    from io import StringIO
    old_stderr = sys.stderr
    sys.stderr = captured_stderr = StringIO()
    
    try:
        # Try to import TTS
        from TTS.api import TTS
        print("✅ Coqui TTS imported successfully")
        
        # Test loading a Portuguese model
        print("🔄 Testing Portuguese model loading...")
        tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)
        print("✅ Portuguese model loaded successfully")
        
        # Test synthesis
        test_text = "Olá, este é um teste de síntese de voz em português."
        tts.tts_to_file(text=test_text, file_path="test_output.wav")
        print("✅ Synthesis completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    finally:
        # Restore stderr
        sys.stderr = old_stderr

def install_with_pip():
    """Install Coqui TTS with pip using specific versions"""
    print("🚀 Installing Coqui TTS with specific versions...")
    
    try:
        # Use subprocess to run pip install with specific versions
        cmd = [
            sys.executable, "-m", "pip", "install",
            "TTS==0.21.0",
            "inflect==5.6.2",
            "pydantic==1.10.22",
            "--no-cache-dir"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Coqui TTS installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def main():
    """Main function to fix Coqui TTS issues"""
    print("🔧 Comprehensive Coqui TTS Fix for Windows")
    print("=" * 50)
    
    # First try to test with current installation
    if test_import_with_fixes():
        print("🎉 Coqui TTS is already working with fixes!")
        return True
    
    # If that fails, try to reinstall
    print("🔧 Coqui TTS needs to be reinstalled...")
    
    if install_with_pip():
        if test_import_with_fixes():
            print("🎉 Coqui TTS fixed successfully!")
            return True
        else:
            print("❌ Coqui TTS still not working after installation")
            return False
    else:
        print("❌ Failed to install Coqui TTS")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All fixes applied successfully!")
        print("You can now use Coqui TTS in your application.")
    else:
        print("\n❌ Some fixes failed.")
        print("Please check the error messages above.")
        sys.exit(1)