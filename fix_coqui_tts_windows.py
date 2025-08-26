#!/usr/bin/env python3
"""
Fix Coqui TTS Installation on Windows
This script helps resolve common issues with Coqui TTS on Windows systems,
particularly the MeCab dependency problems.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def fix_mecab_issues():
    """Apply fixes for MeCab issues on Windows"""
    print("🔧 Applying MeCab fixes for Windows...")
    
    # Set environment variables to bypass MeCab
    os.environ['MECAB_PATH'] = ''
    os.environ['MECAB_CHARSET'] = 'utf8'
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Create a dummy mecabrc file to prevent the error
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
    
    print("✅ MeCab fixes applied")

def install_coqui_tts_with_fixes():
    """Install Coqui TTS with Windows-specific fixes"""
    print("🚀 Installing Coqui TTS with Windows fixes...")
    
    # Apply MeCab fixes first
    fix_mecab_issues()
    
    try:
        # Install with specific versions that work better on Windows
        cmd = [
            sys.executable, "-m", "pip", "install",
            "TTS>=0.21.0",  # Updated version
            "torch>=1.13.0",
            "torchaudio>=0.13.0",
            "--no-cache-dir",
            "--force-reinstall"
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

def test_coqui_tts():
    """Test if Coqui TTS works after fixes"""
    print("🧪 Testing Coqui TTS...")
    
    # Apply environment fixes
    fix_mecab_issues()
    
    try:
        # Suppress warnings and errors
        import warnings
        warnings.filterwarnings('ignore')
        
        # Import with error handling
        import sys
        from io import StringIO
        
        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        
        # Import TTS outside the inner try block to ensure it's available
        from TTS.api import TTS
        
        try:
            # Try to load a simple model that doesn't require MeCab
            tts_instance = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)
            print("✅ Coqui TTS is working correctly with YourTTS model")
            return True
            
        except Exception as e:
            if "MeCab" in str(e) or "mecab" in str(e).lower():
                print("⚠️ MeCab issue detected - applying additional fixes")
                # Try to load a model that doesn't require MeCab
                try:
                    # Try XTTS v2 model which is more robust
                    tts_instance = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
                    print("✅ Coqui TTS is working with XTTS v2 model")
                    return True
                except Exception as e2:
                    print(f"❌ Coqui TTS still not working with XTTS v2: {e2}")
                    return False
            else:
                print(f"❌ Coqui TTS test failed: {e}")
                return False
        finally:
            sys.stderr = old_stderr
            
    except ImportError as import_error:
        print(f"❌ Coqui TTS not installed: {import_error}")
        return False
    except Exception as e:
        print(f"❌ Coqui TTS test error: {e}")
        return False

def create_coqui_config():
    """Create configuration files for Coqui TTS"""
    print("📝 Creating Coqui TTS configuration...")
    
    config_content = """
# Coqui TTS Configuration for Windows
[general]
sample_rate = 22050
language = pt-BR

[model]
default_model = tts_models/multilingual/multi-dataset/xtts_v2
fallback_model = tts_models/multilingual/multi-dataset/your_tts

[performance]
use_gpu = false
progress_bar = false
"""
    
    config_path = Path("coqui_tts_config.ini")
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✅ Configuration file created at {config_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return False

def main():
    """Main function to fix Coqui TTS issues"""
    print("🔧 Coqui TTS Windows Fixer")
    print("=" * 40)
    
    # Check if we're in the correct directory
    if not os.path.exists("requirements_enhanced.txt"):
        print("⚠️ Please run this script from the project root directory")
        return False
    
    # Apply all fixes
    fix_mecab_issues()
    
    # Test current installation
    if test_coqui_tts():
        print("🎉 Coqui TTS is already working!")
        create_coqui_config()
        return True
    
    # If not working, try to reinstall
    print("🔧 Coqui TTS needs to be reinstalled...")
    
    if install_coqui_tts_with_fixes():
        if test_coqui_tts():
            print("🎉 Coqui TTS fixed successfully!")
            create_coqui_config()
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
        print("Try starting the server with: start_enhanced_with_fix.bat")
    else:
        print("\n❌ Some fixes failed.")
        print("Please check the error messages above.")
        print("As a fallback, the system will use pyttsx3/gTTS engines.")
        sys.exit(1)