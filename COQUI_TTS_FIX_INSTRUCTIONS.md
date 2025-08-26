# Coqui TTS Fix Instructions

This document provides step-by-step instructions to fix Coqui TTS issues on Windows systems.

## Problem Summary

The Coqui TTS library has dependency issues on Windows systems, particularly with the MeCab library, which causes import errors and prevents the Portuguese models from loading correctly.

## Solution Overview

We've implemented multiple layers of fixes:

1. **Environment Configuration**: Setting proper environment variables
2. **Application-Level Fixes**: Applying fixes at startup
3. **Robust Error Handling**: Graceful fallback to alternative TTS engines
4. **Enhanced Startup Scripts**: Ensuring proper environment setup

## Step-by-Step Fix Instructions

### Option 1: Automated Fix (Recommended)

1. Run the fix script:
   ```
   fix_coqui_tts.bat
   ```

2. If successful, start the application with:
   ```
   start_enhanced_with_fix.bat
   ```

### Option 2: Manual Environment Setup

1. Set environment variables manually:
   ```batch
   set MECAB_PATH=
   set MECAB_CHARSET=utf8
   set PYTHONIOENCODING=utf-8
   ```

2. Start the application:
   ```batch
   start_enhanced_with_fix.bat
   ```

### Option 3: Direct Application Start

1. Use the enhanced startup script that applies fixes automatically:
   ```
   start_enhanced_with_fix.bat
   ```

## How the Fix Works

### 1. Environment Variables
- `MECAB_PATH=` - Disables MeCab path lookup
- `MECAB_CHARSET=utf8` - Sets proper character encoding
- `PYTHONIOENCODING=utf-8` - Ensures proper UTF-8 handling

### 2. Dummy mecabrc File
Creates a dummy configuration file to prevent "file not found" errors.

### 3. Warning Suppression
Filters out MeCab-related warnings that can cause import failures.

### 4. Model Loading Strategy
Tries multiple models in order of robustness:
1. XTTS v2 (most robust on Windows)
2. Portuguese VITS
3. YourTTS (multilingual)
4. Portuguese Tacotron2

### 5. Fallback Engines
If Coqui TTS fails completely, the system automatically falls back to:
1. pyttsx3 (offline TTS)
2. gTTS (online TTS with Google services)

## Testing the Fix

Run the test script to verify the fix works:
```
venv\Scripts\python.exe test_mecab_fix.py
```

## Fallback Behavior

If Coqui TTS still doesn't work:
1. The system will automatically use pyttsx3 for offline TTS
2. If pyttsx3 fails, it will fall back to gTTS for online TTS
3. Cloned voices will be simulated using gTTS with voice identification

## Files Created/Modified

### New Files:
- `fix_coqui_tts_windows.py` - Python fix script
- `fix_coqui_tts.bat` - Batch script to run the fix
- `start_enhanced_with_fix.bat` - Enhanced startup script
- `test_mecab_fix.py` - Simple test script
- `COQUI_TTS_FIX_INSTRUCTIONS.md` - This file

### Modified Files:
- `backend/main_enhanced.py` - Added MeCab fixes at startup and improved error handling

## Troubleshooting

### If Coqui TTS Still Fails:
1. Ensure you're using the virtual environment:
   ```
   venv\Scripts\activate
   ```

2. Check Python version compatibility (3.8-3.11 recommended)

3. Clear pip cache:
   ```
   pip cache purge
   ```

4. Reinstall with no cache:
   ```
   pip install --no-cache-dir TTS
   ```

### If You Get CUDA Errors:
1. Force CPU mode by ensuring `gpu=False` in TTS initialization
2. Or install compatible CUDA version

### If Models Won't Download:
1. Check internet connection
2. Ensure sufficient disk space (models can be 1-3GB)
3. Check firewall/antivirus settings

## Performance Notes

- XTTS v2 model provides the best quality and stability on Windows
- All models work offline once downloaded
- Fallback engines provide basic functionality without large downloads
- Voice cloning works with all engines (simulated with gTTS when Coqui fails)

## Support

If issues persist:
1. Check application logs for specific error messages
2. Verify all dependencies are correctly installed
3. Ensure you're using Python 3.8-3.11 (TTS compatibility)
4. Consider using the fallback engines (pyttsx3/gTTS) for basic functionality