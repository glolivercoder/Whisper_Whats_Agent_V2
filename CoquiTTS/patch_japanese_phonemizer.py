#!/usr/bin/env python3
"""
Patch script to modify the Japanese phonemizer to handle MeCab import gracefully
"""

import os
import sys
import shutil
from pathlib import Path

def patch_japanese_phonemizer():
    """Patch the Japanese phonemizer to handle MeCab import gracefully"""
    try:
        # Find the TTS installation
        import TTS
        tts_path = Path(TTS.__file__).parent
        japanese_phonemizer_path = tts_path / "tts" / "utils" / "text" / "japanese" / "phonemizer.py"
        
        if not japanese_phonemizer_path.exists():
            print(f"❌ Japanese phonemizer not found at {japanese_phonemizer_path}")
            return False
            
        # Read the original file
        with open(japanese_phonemizer_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already patched
        if "# PATCHED FOR WINDOWS" in content:
            print("✅ Japanese phonemizer already patched")
            return True
            
        # Backup the original file
        backup_path = japanese_phonemizer_path.with_suffix('.py.bak')
        shutil.copy2(japanese_phonemizer_path, backup_path)
        print(f"✅ Backup created at {backup_path}")
        
        # Modify the MeCab import section
        lines = content.split('\n')
        patched_lines = []
        
        mecab_import_found = False
        for line in lines:
            if "import MeCab" in line and "ImportError" in line:
                mecab_import_found = True
                # Replace the problematic import with a safe version
                patched_lines.append("# PATCHED FOR WINDOWS - Safe MeCab import")
                patched_lines.append("try:")
                patched_lines.append("    import MeCab")
                patched_lines.append("except ImportError as e:")
                patched_lines.append("    # Handle MeCab import gracefully on Windows")
                patched_lines.append("    import os")
                patched_lines.append("    if os.environ.get('COQUI_TTS_NO_MECAB') == '1':")
                patched_lines.append("        MeCab = None  # Skip MeCab when explicitly disabled")
                patched_lines.append("    else:")
                patched_lines.append("        raise ImportError('Japanese requires mecab-python3 and unidic-lite.') from e")
            elif mecab_import_found and "raise ImportError" in line:
                # Skip the original error message
                continue
            else:
                patched_lines.append(line)
        
        if not mecab_import_found:
            print("⚠️ MeCab import section not found - patching differently")
            # Alternative approach - add at the beginning
            patched_content = content.replace(
                'try:\n    import MeCab\nexcept ImportError as e:\n    raise ImportError("Japanese requires mecab-python3 and unidic-lite.") from e',
                '# PATCHED FOR WINDOWS - Safe MeCab import\n'
                'try:\n    import MeCab\nexcept ImportError as e:\n'
                '    import os\n'
                '    if os.environ.get("COQUI_TTS_NO_MECAB") == "1":\n'
                '        MeCab = None  # Skip MeCab when explicitly disabled\n'
                '    else:\n'
                '        raise ImportError("Japanese requires mecab-python3 and unidic-lite.") from e'
            )
        else:
            patched_content = '\n'.join(patched_lines)
        
        # Write the patched file
        with open(japanese_phonemizer_path, 'w', encoding='utf-8') as f:
            f.write(patched_content)
            
        print(f"✅ Japanese phonemizer patched successfully at {japanese_phonemizer_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error patching Japanese phonemizer: {e}")
        return False

def test_patch():
    """Test if the patch works"""
    print("🧪 Testing patched Japanese phonemizer...")
    
    # Set environment variable to skip MeCab
    os.environ['COQUI_TTS_NO_MECAB'] = '1'
    
    try:
        # Try to import the Japanese phonemizer
        from TTS.tts.utils.text.japanese.phonemizer import JA_JP_Phonemizer
        print("✅ Japanese phonemizer imported successfully (MeCab skipped)")
        return True
    except Exception as e:
        print(f"❌ Error importing Japanese phonemizer: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Patching Japanese Phonemizer for Windows")
    print("=" * 40)
    
    success = patch_japanese_phonemizer()
    
    if success:
        test_success = test_patch()
        if test_success:
            print("\n🎉 Japanese phonemizer patched successfully!")
            print("You can now use Coqui TTS without MeCab issues on Windows.")
        else:
            print("\n❌ Patch applied but test failed")
    else:
        print("\n❌ Failed to patch Japanese phonemizer")