# Coqui TTS Fix Summary

This document summarizes all the changes and files created to fix Coqui TTS issues on Windows systems.

## Files Created

### 1. Fix Scripts
- `fix_coqui_tts_windows.py` - Python script to fix Coqui TTS installation
- `fix_coqui_tts.bat` - Batch file to run the fix script
- `start_with_coqui_fix.bat` - Startup script with environment fixes

### 2. Test Scripts
- `test_coqui_tts_fix.py` - Script to verify fixes work correctly

### 3. Documentation
- `COQUI_TTS_WINDOWS_FIX.md` - Comprehensive guide for fixing Coqui TTS on Windows
- Updated `README.md` - Added information about Coqui TTS fixes

## Code Changes Made

### 1. Backend Application (`backend/main_enhanced.py`)
- Added MeCab fixes at application startup
- Updated model loading order to prioritize XTTS v2
- Enhanced error handling for Coqui TTS loading
- Added XTTS v2 to available models list

### 2. TTS Service Improvements
- Added XTTS v2 as the first model to try (more robust on Windows)
- Improved fallback behavior when models fail to load
- Better error logging and reporting

## Solution Overview

The main issues with Coqui TTS on Windows were:
1. **MeCab dependency errors** preventing import of TTS modules
2. **Model loading failures** for Portuguese models
3. **Import-time errors** that couldn't be caught by application code

### Applied Fixes

1. **Environment Configuration**:
   - Set `MECAB_PATH=` and `MECAB_CHARSET=utf8` to bypass MeCab
   - Added `PYTHONIOENCODING=utf-8` for proper encoding
   - Created dummy `mecabrc` file to prevent file not found errors

2. **Import Protection**:
   - Applied fixes at application startup before any TTS imports
   - Added warning filters to suppress MeCab-related warnings
   - Used stderr capture to prevent MeCab error messages

3. **Model Fallback Strategy**:
   - Try XTTS v2 first (most robust on Windows)
   - Fall back to Portuguese VITS model
   - Then try YourTTS multilingual model
   - Finally fall back to pyttsx3/gTTS if all Coqui models fail

4. **Enhanced Error Handling**:
   - Better logging of model loading failures
   - Automatic fallback to alternative engines
   - Simulation mode for cloned voices when Coqui fails

## Usage Instructions

### Quick Fix
Run the provided batch file:
```batch
fix_coqui_tts.bat
```

### Start with Fixes Applied
Use the enhanced startup script:
```batch
start_with_coqui_fix.bat
```

### Manual Application
Set environment variables manually:
```batch
set MECAB_PATH=
set MECAB_CHARSET=utf8
set PYTHONIOENCODING=utf-8
```

## Testing

Verify the fixes work with:
```bash
python test_coqui_tts_fix.py
```

## Fallback Behavior

If Coqui TTS still fails:
1. System automatically falls back to pyttsx3 (offline)
2. If pyttsx3 fails, falls back to gTTS (online)
3. Cloned voices are simulated using gTTS with voice identification

## Models Available

1. **XTTS v2** (`tts_models/multilingual/multi-dataset/xtts_v2`) - Most robust
2. **Portuguese VITS** (`tts_models/pt/cv/vits`) - High quality Portuguese
3. **YourTTS** (`tts_models/multilingual/multi-dataset/your_tts`) - Multilingual with voice cloning
4. **Portuguese Tacotron2** (`tts_models/pt/cv/tacotron2-DDC`) - Alternative Portuguese model

## Performance Notes

- XTTS v2 provides the best quality and stability on Windows
- All models work offline once downloaded (600MB-2GB depending on model)
- Models are downloaded to user's home directory automatically
- Fallback engines provide basic functionality without large downloads

## Troubleshooting

If issues persist:
1. Check application logs for specific error messages
2. Ensure virtual environment is activated
3. Verify Python version compatibility (3.8-3.11 recommended)
4. Clear pip cache: `pip cache purge`
5. Reinstall with no cache: `pip install --no-cache-dir TTS`