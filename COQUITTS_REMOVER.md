# Coqui TTS and Voice Cloning Removal Guide

This document lists all the files, directories, database tables, and configurations that need to be removed to completely eliminate the Coqui TTS and voice cloning functionality from the project.

## 1. Directories to be removed

The following directories are entirely related to TTS and voice cloning and can be safely deleted:

- `cloned_voices/`
- `CoquiTTS/`
- `coquittsbasic/`
- `reference_audio/`

## 2. Files to be removed

The following files are related to TTS, Coqui, XTTS, and voice cloning. They should be deleted.

### Analysis and Debugging Files
- `analyze_coqui_models_portuguese.py`
- `debug_audio_generation_deep.py`
- `debug_real_cloning_detailed.py`
- `debug_voice_cloning_deep_analysis.py`
- `debug_voice_cloning_issue.py`
- `implement_real_voice_cloning.py`
- `inspect_xtts_languages.py`
- `inspect_xtts_model.py`
- `inspect_xtts_parameters.py`
- `simple_xtts_test.py`

### Fix and Patch Files
- `apply_final_tts_fixes.py`
- `apply_final_xtts_v2_fix.py`
- `apply_tts_fixes_carefully.py`
- `fix_coqui_*.py` (all files starting with `fix_coqui_`)
- `fix_mecab_*.py` (all files starting with `fix_mecab_`)
- `fix_tts_*.py` (all files starting with `fix_tts_`)
- `fix_voice_cloning_*.py` (all files starting with `fix_voice_cloning_`)
- `fix_xtts_*.py` (all files starting with `fix_xtts_`)
- `xtts_fixed_implementation.py`
- `xtts_voice_cloner_final.py`

### Test Files
- `test_coqui_*.py` (all files starting with `test_coqui_`)
- `test_cloned_voice_fix.py`
- `test_cloned_voices_endpoint.py`
- `test_delete_cloned_voice.py`
- `test_direct_tts.py`
- `test_mecab_fix.bat`
- `test_mecab_fix.py`
- `test_no_mecab.bat`
- `test_real_voice_cloning_final.py`
- `test_tortoise_fix_final.py`
- `test_tts_*.py` (all files starting with `test_tts_`)
- `test_voice_cloning_*.py` (all files starting with `test_voice_cloning_`)
- `test_voices_simple.py`
- `test_with_real_voice_*.py`
- `test_without_mecab.py`
- `test_xtts_*.py` (all files starting with `test_xtts_`)

### Configuration and Integration Files
- `check_voice_cloning_setup.py`
- `clone_voice_exact_replica.py`
- `configure_xtts_v2_default.py`
- `coqui_backend_fix_working.py`
- `coqui_tts_config.ini`
- `integrate_coquitts_basic.py`
- `integrate_working_voice_cloning.py`
- `requirements_voice_cloning.txt`
- `restart_server_with_voice_cloning.py`

### Documentation and Summary Files
- `CLONED_VOICES_IMPROVEMENT_GUIDE.md`
- `CLONED_VOICES_IMPROVEMENTS_SUMMARY.md`
- `comparacao_coqui_detalhada.py`
- `COQUI_TTS_FIX_INSTRUCTIONS.md`
- `COQUI_TTS_FIX_SUMMARY_FINAL.md`
- `COQUI_TTS_FIX_SUMMARY.md`
- `COQUI_TTS_STATUS_FINAL.md`
- `COQUI_TTS_WINDOWS_FIX.md`
- `VOICE_DELETION_SUMMARY.md`
- `XTTS_V2_FIX_FINAL_SUMMARY.md`
- `XTTS_V2_IMPLEMENTATION_SUMMARY.md`
- `XTTS_V2_LIBRARIES_VERIFICATION.md`
- `XTTS_V2_LIBRARY_VERIFICATION_RESPONSE.md`

### Scripts
- `remove_mecab_final.bat`
- `start_enhanced_voice_cloning.bat`
- `start_with_coqui_fix.bat`
- `start_with_xtts_v2_fixes.bat`
- `start_with_xtts_v2.bat`
- `start_with_xtts_v2.py`
- `start_xtts_v2.bat`

## 3. Database Schema

The database schema is defined in `backend/main_enhanced.py` in the `DatabaseService` class. There are no specific tables for TTS or voice cloning. The conversation logs and other tables are generic and do not need to be removed.

## 4. Code and Configuration to be removed

The following files still contain code or configuration related to TTS that needs to be removed.

### `backend/main_enhanced.py`
- The `TTSRequest` Pydantic model should be removed (Already done).
- The `TTSService` class should be removed (Already done).
- The `tts_service` initialization should be removed (Already done).
- All TTS and voice cloning endpoints should be removed (Already done).
- The `CloningTool` class should be removed (Already done).
- In the `health_check` endpoint, the `tts_service` section should be removed (Already done).
- In the `chat` endpoint, the logic for TTS synthesis should be removed (Already done).
- In the `websocket_endpoint`, the TTS related logic should be removed (Partially done, user canceled the last operation).
- In the `Config` class, the following lines should be removed:
  ```python
  # TTS Configuration  
  self.TTS_ENABLED = os.getenv("TTS_ENABLED", "true").lower() == "true"
  self.TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "pt-BR")
  self.TTS_VOICE = os.getenv("TTS_VOICE", "pt-BR-Wavenet-A")
  ```
- In the `ChatMessage` Pydantic model, the following lines should be removed:
  ```python
  use_tts: Optional[bool] = True
  tts_engine: Optional[str] = "coqui"  # Default to Coqui TTS
  tts_voice: Optional[str] = None  # Add voice selection
  ```

### `templates/index_enhanced.html`
- The "TTS & Voice" tab and its content have been removed (Already done).
- The javascript functions related to TTS and voice cloning have been removed (Already done).

### `requirements.txt`
- The following packages should be removed:
  - `pydub==0.25.1`
  - `soundfile==0.12.1`
  - `librosa==0.10.1`

### `requirements_enhanced.txt`
- The following packages should be removed:
  - `pyttsx3>=2.90`
  - `gTTS>=2.3.0`
  - `TTS>=0.13.0`
  - `torch>=1.11.0`
  - `torchaudio>=0.11.0`
  - `inflect>=5.6.0`
  - `numba>=0.56.0`
  - `mecab-python3>=1.0.4`
  - `librosa`
  - `soundfile`