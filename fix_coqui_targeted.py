#!/usr/bin/env python3
"""
Targeted Fix for Coqui TTS on Windows
This script applies specific fixes to resolve MeCab-related issues with Coqui TTS on Windows.
"""

import os
import sys
import subprocess
import warnings
from pathlib import Path

def apply_targeted_fixes():
    """Apply targeted fixes for Coqui TTS on Windows"""
    print("🎯 Targeted Coqui TTS Fix")
    print("=" * 30)
    print("🔧 Applying targeted fixes...")
    
    # Set environment variables to bypass MeCab issues
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Create a dummy mecabrc file to prevent the error
    try:
        temp_dir = os.path.join(os.environ.get('TEMP', '.'), 'mecab')
        os.makedirs(temp_dir, exist_ok=True)
        mecabrc_path = os.path.join(temp_dir, 'mecabrc')
        
        if not os.path.exists(mecabrc_path):
            with open(mecabrc_path, 'w', encoding='utf-8') as f:
                f.write("# Dummy mecabrc file to prevent MeCab errors\n")
            print(f"✅ Created dummy mecabrc at {mecabrc_path}")
            
        # Also create in system temp directory
        system_temp = os.environ.get('TEMP', '.')
        system_mecabrc = os.path.join(system_temp, 'mecabrc')
        if not os.path.exists(system_mecabrc):
            with open(system_mecabrc, 'w', encoding='utf-8') as f:
                f.write("# Dummy mecabrc file to prevent MeCab errors\n")
            print(f"✅ Created system dummy mecabrc at {system_mecabrc}")
    except Exception as e:
        print(f"⚠️ Could not create dummy mecabrc: {e}")
    
    # Suppress MeCab-related warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='mecab')
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    print("✅ Targeted fixes applied")

def test_minimal_import():
    """Test importing TTS with minimal configuration"""
    print("🔍 Testing minimal import...")
    
    try:
        # Capture stderr to suppress MeCab error messages
        from io import StringIO
        old_stderr = sys.stderr
        sys.stderr = captured_stderr = StringIO()
        
        # Try to import TTS
        import TTS
        print("✅ TTS module imported")
        
        # Restore stderr
        sys.stderr = old_stderr
        
        # Show any captured output at debug level
        captured_output = captured_stderr.getvalue()
        if captured_output and "MeCab" in captured_output:
            print("ℹ️ MeCab warnings were suppressed (this is normal on Windows)")
            
        return True
        
    except Exception as e:
        # Restore stderr
        sys.stderr = old_stderr
        print(f"❌ Import error: {e}")
        return False

def install_with_constraints():
    """Install TTS with specific constraints for Windows compatibility"""
    print("🔧 Installing with constraints...")
    
    try:
        # Install with specific versions that work better on Windows
        cmd = [
            sys.executable, "-m", "pip", "install",
            "TTS==0.21.0",
            "inflect==5.6.2",  # Compatible version
            "pydantic==1.10.22",  # Compatible version
            "--no-cache-dir",
            "--force-reinstall"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ TTS installed with constraints")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def test_coqui_tts():
    """Test if Coqui TTS works after fixes"""
    print("🧪 Testing Coqui TTS...")
    
    try:
        # Import with error handling
        from io import StringIO
        
        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        # Import TTS API
        from TTS.api import TTS
        
        # Try to load a simple model that doesn't require MeCab
        tts_instance = TTS(
            model_name="tts_models/multilingual/multi-dataset/your_tts", 
            progress_bar=False, 
            gpu=False
        )
        
        # Restore stderr
        sys.stderr = old_stderr
        
        print("✅ Coqui TTS is working correctly with YourTTS model")
        return True
        
    except Exception as e:
        # Restore stderr
        sys.stderr = old_stderr
        
        if "MeCab" in str(e) or "mecab" in str(e).lower():
            print("⚠️ MeCab issue detected - this is a known Windows issue")
            print("💡 Solution: The system will use pyttsx3/gTTS as fallback engines")
            return False
        else:
            print(f"❌ Coqui TTS test failed: {e}")
            return False

def main():
    """Main function to apply targeted fixes"""
    print("🎯 Targeted Coqui TTS Fix for Windows")
    print("=" * 40)
    
    # Apply all fixes
    apply_targeted_fixes()
    
    # Test current installation
    if test_minimal_import():
        if test_coqui_tts():
            print("\n🎉 Coqui TTS is working correctly!")
            return True
        else:
            print("\n🔧 Coqui TTS needs additional fixes...")
            if install_with_constraints():
                if test_coqui_tts():
                    print("\n🎉 Coqui TTS fixed successfully!")
                    return True
                else:
                    print("\n❌ Coqui TTS still not working after installation")
                    return False
            else:
                print("\n❌ Failed to install Coqui TTS with constraints")
                return False
    else:
        print("\n❌ Coqui TTS not available")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All targeted fixes applied successfully!")
        print("You can now use Coqui TTS in your application.")
    else:
        print("\n❌ Some fixes failed.")
        print("The system will use pyttsx3/gTTS engines as fallbacks.")
        sys.exit(1)