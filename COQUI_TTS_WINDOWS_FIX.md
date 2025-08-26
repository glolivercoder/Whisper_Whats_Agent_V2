# Coqui TTS Windows Fix Guide

This guide helps resolve common issues with Coqui TTS on Windows systems, particularly the MeCab dependency problems that prevent the Portuguese models from loading correctly.

## Common Issues

1. **MeCab Runtime Error**: `Failed initializing MeCab. Please see the README for possible solutions`
2. **Import Errors**: Cannot import TTS modules due to MeCab dependencies
3. **Model Loading Failures**: Portuguese models fail to load on Windows

## Solution Overview

The fix involves:
1. Setting environment variables to bypass MeCab
2. Using specific model loading order that works on Windows
3. Implementing proper error handling and fallbacks

## Automated Fix

Run the provided fix script:

```batch
fix_coqui_tts.bat
```

This script will:
1. Activate your virtual environment
2. Set required environment variables
3. Run the Python fix script
4. Test the installation

## Manual Fix Steps

If you prefer to fix manually:

### 1. Set Environment Variables

```batch
set MECAB_PATH=
set MECAB_CHARSET=utf8
```

### 2. Update requirements.txt

Ensure you have the correct versions:
```txt
TTS>=0.13.0
torch>=1.11.0
torchaudio>=0.11.0
```

### 3. Reinstall Coqui TTS

```bash
pip uninstall TTS
pip install TTS torch torchaudio --no-cache-dir
```

## Model Loading Order

The application now tries models in this order:
1. `tts_models/multilingual/multi-dataset/xtts_v2` (Most robust)
2. `tts_models/pt/cv/vits` (Portuguese VITS)
3. `tts_models/multilingual/multi-dataset/your_tts` (Multilingual)
4. `tts_models/pt/cv/tacotron2-DDC` (Portuguese Tacotron2)

## Testing the Fix

After applying the fix, test with:

```python
import os
os.environ['MECAB_PATH'] = ''
os.environ['MECAB_CHARSET'] = 'utf8'

from TTS.api import TTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
print("Coqui TTS loaded successfully!")
```

## Fallback Behavior

If Coqui TTS fails to load:
1. The system automatically falls back to pyttsx3 (offline)
2. If pyttsx3 fails, it falls back to gTTS (online)
3. Cloned voices are simulated using gTTS with voice identification

## Additional Tips

1. **Use XTTS v2**: This model is more robust on Windows and supports multiple languages
2. **Disable GPU**: Forcing CPU mode prevents CUDA-related issues
3. **Progress Bar**: Disabling progress bar prevents display issues in some environments
4. **Virtual Environment**: Always use a virtual environment to avoid dependency conflicts

## Troubleshooting

### If MeCab errors persist:
1. Install Visual C++ Redistributables
2. Check Windows PATH environment variable
3. Ensure no conflicting MeCab installations

### If models still won't load:
1. Clear pip cache: `pip cache purge`
2. Reinstall with no cache: `pip install --no-cache-dir TTS`
3. Check available models: `tts --list_models`

### If you get CUDA errors:
1. Ensure compatible CUDA version
2. Or force CPU mode: `gpu=False` in TTS initialization

## Performance Notes

- XTTS v2 model provides the best quality and stability on Windows
- Portuguese VITS model is smaller and faster but may have MeCab issues
- YourTTS model is multilingual but larger
- All models work offline once downloaded

## File Locations

- **Models**: Downloaded to `~/.local/share/tts/` (Linux/Mac) or `%USERPROFILE%\.local\share\tts\` (Windows)
- **Configuration**: Application uses built-in configuration
- **Logs**: Check application logs for detailed error information

## Support

If issues persist:
1. Check the application logs for specific error messages
2. Verify all dependencies are correctly installed
3. Ensure you're using Python 3.8-3.11 (TTS compatibility)
4. Consider using the fallback engines (pyttsx3/gTTS) for basic functionality