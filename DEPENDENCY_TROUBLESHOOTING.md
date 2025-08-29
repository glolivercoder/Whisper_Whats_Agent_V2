# 🔧 DEPENDENCY CONFLICTS RESOLUTION

## ⚠️ Common Issues and Fixes

If you see errors like:
```
faster-whisper 1.0.1 requires tokenizers<0.16,>=0.13, but you have tokenizers 0.21.4
tortoise-tts 3.0.0 requires transformers==4.31.0, but you have transformers 4.55.4
```

Your TTS functionality may be broken. Here's how to fix it:

---

## 🚀 QUICK FIX (Recommended)

### Step 1: Run the Automated Fixer
```bash
./setup_tts_clean.bat
```

This script will:
- ✅ Remove conflicting packages
- ✅ Install correct versions in proper order
- ✅ Test the installation
- ✅ Verify TTS functionality

### Step 2: Manual Verification
```bash
# Test if TTS imports work
python -c "from TTS.api import TTS; print('✅ TTS ready!')"

# Test tokenizers version
python -c "import tokenizers; print('Tokenizers:', tokenizers.__version__)"

# Test transformers version
python -c "import transformers; print('Transformers:', transformers.__version__)"
```

---

## 🛠️ MANUAL FIX (Alternative)

If the automated script doesn't work, follow these steps:

### 1. Clean Conflicting Packages
```bash
pip uninstall -y tokenizers transformers tortoise-tts
```

### 2. Install in Correct Order
```bash
# Order matters!
pip install tokenizers==0.13.3
pip install transformers==4.31.0
pip install faster-whisper==1.0.1
pip install pydub==0.25.1
pip install ffmpeg-python==0.2.0
pip install "TTS==0.22.0"  # Note: quotes are important!
```

### 3. Test Installation
```bash
python test_tts_integration.py
```

---

## 📋 VERIFIED COMPATIBLE VERSIONS

| Package | Version | Why this version? |
|---------|---------|-------------------|
| `tokenizers` | `0.13.3` | Required by faster-whisper |
| `transformers` | `4.31.0` | Required by TTS/CoquiTTS |
| `faster-whisper` | `1.0.1` | Latest stable for this pipeline |
| `TTS` | `0.22.0` | Stable version with voice cloning |
| `pydub` | `0.25.1` | Audio processing |
| `ffmpeg-python` | `0.2.0` | Format conversion |

---

## 🔍 DIAGNOSTICS

### Run Dependency Checker
```bash
python check_dependencies.py
```

This will:
- 🔍 Scan for version conflicts
- 📝 Generate fix commands
- 🛠️ Create repair scripts automatically

### Expected Output:
```
🔍 Checking for dependency conflicts...
✅ tokenizers version correct
✅ transformers version correct
✅ TTS import successful
✅ No conflicts found!
```

---

## 🚨 KNOWN ISSUES

### Issue 1: TORTOISE-TTS Conflicts
**Problem:** tortoise-tts installs incompatible versions
**Solution:** Always remove tortoise-tts before installing TTS

### Issue 2: Order Matters
**Problem:** Installing TTS first causes tokenizers issues
**Solution:** Always install tokenizers → transformers → TTS

### Issue 3: GPU Issues (optional)
**Problem:** PyTorch GPU conflicts with CPU environments
**Solution:** Default to CPU mode, add GPU packages if needed

---

## 🎯 ALTERNATIVE VERSIONS

If the main fix doesn't work, try these alternatives:

### Option A: Legacy Stable
```bash
pip install tokenizers==0.13.3
pip install transformers==4.31.0
pip install TTS==0.21.3
```

### Option B: More Conservative
```bash
pip install tokenizers==0.13.2
pip install transformers==4.30.0
pip install TTS==0.20.6
```

---

## 🧪 TESTING YOUR FIX

### 1. Test TTS Import
```bash
python -c "
from TTS.api import TTS
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
print('✅ TTS initialization successful!')
"
```

### 2. Test Voice Synthesis
```bash
python -c "
from TTS.api import TTS
import tempfile
import os

tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)

with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
    output_path = f.name

try:
    tts.tts_to_file(text='Olá, testes de voz!', file_path=output_path)
    if os.path.exists(output_path):
        print(f'✅ Audio generated successfully: {output_path}')
    else:
        print('❌ Audio file not created')
finally:
    if os.path.exists(output_path):
        os.unlink(output_path)
"
```

### 3. Run Full Integration Test
```bash
python test_tts_integration.py
```

---

## 🌟 SUCCESS CRITERIA

Your TTS setup is working when:

✅ **Python imports work**
```python
from TTS.api import TTS
```

✅ **Model loads correctly**
```python
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')
```

✅ **Audio is generated**
```python
tts.tts_to_file(text='Hello', file_path='test.wav')
```

✅ **No version conflicts**
```bash
pip check  # Should show no conflicts
```

---

## 📞 SUPPORT

If you're still having issues:

1. **Clean reinstall** - Remove virtual environment and create a new one
2. **Check logs** - Look at detailed error messages
3. **System requirements** - Ensure you have adequate RAM/disk space
4. **Platform differences** - Windows/Mac/Linux specific issues

---

**Status: 🔧 Ready to fix TTS dependency conflicts**