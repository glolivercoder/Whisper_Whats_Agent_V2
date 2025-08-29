# 🔊 CoquiTTS VoxClone Integration

## Overview
The CoquiTTS VoxClone feature has been successfully integrated into the WhatsApp Voice Agent V2 application. This provides advanced text-to-speech synthesis with voice cloning capabilities.

## Features
### 🎤 Speech Synthesis
- **Multiple Models**: XTTS v2, YourTTS, Tacotron2, and more
- **Voice Cloning**: Use reference audio samples to clone voices
- **Multi-language**: Portuguese, English, Spanish, French, and more
- **Audio Formats**: WAV, MP3, OGG output
- **GPU/CPU Support**: Configurable device selection

### 🎵 Voice Profiles
- **Save Voice Profiles**: Create and save custom voice profiles
- **Profile Management**: Load, edit, and delete saved profiles
- **Reference Audio**: Upload or use existing audio samples
- **Gender Classification**: Organize profiles by gender

## User Interface
### Frontend Tab
- **New Tab Added**: "🔊 CoquiTTS VoxClone" in the main navigation
- **Intuitive Controls**: Model selection, text input, audio preview
- **Progress Tracking**: Real-time synthesis progress
- **Audio Player**: Built-in audio playback and download

### Backend API
```
POST /api/tts/generate           # Generate TTS audio
GET  /api/tts/audio/{filename}   # Serve generated audio
GET  /api/tts/profiles           # Get voice profiles
POST /api/tts/save-profile       # Save voice profile
DELETE /api/tts/profile/{id}     # Delete profile
```

## Quick Start

### 1. Install Dependencies
```bash
pip install TTS pydub ffmpeg-python
```

### 2. First Test
1. Open the application in your browser
2. Navigate to the "🔊 CoquiTTS VoxClone" tab
3. Select a model (e.g., Portuguese XTTS v2)
4. Enter some text
5. Click "Gerar Áudio"
6. Listen and download the result

### 3. Voice Cloning
1. Upload a reference audio file (.wav or .mp3)
2. Choose a compatible model (XTTS v2 or YourTTS)
3. Generate audio - the output will mimic the reference voice
4. Save the profile for future use

## Models and Capabilities

| Model | Language | Voice Cloning | Quality |
|-------|----------|---------------|---------|
| XTTS v2 | Multi/Portuguese | ✅ Full | Excellent |
| YourTTS | Multi/Portuguese | ✅ Full | Very Good |
| Tacotron2 | Single language | ❌ None | Good |
| SpeedySpeech | Single language | ❌ None | Fast |

## Technical Details

### Dependencies Added
```txt
# requirements.txt additions
TTS==0.22.0                # CoquiTTS library
pydub==0.25.1             # Audio format conversion
ffmpeg-python==0.2.0      # Audio processing
```

### Directory Structure
```
/
├── reference_audios/     # Voice samples for cloning
├── generated_audios/     # Generated TTS output
├── tts_profiles.json     # Saved voice profiles
└── coquittsbasic/        # Original project (reference)
    └── Modelos/
        └── perfis/       # Original voice profiles
```

### Automatic Migration
- **Legacy Profiles**: Automatically imports profiles from coquittsbasic
- **Reference Audio**: Copies voice samples to new structure
- **Format Conversion**: Converts older formats automatically

## Configuration

### Environment Settings
```bash
# .env configurations (already set)
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=your-updated-key
```

### TTS-Specific Settings
- **Device**: CPU/GPU selection per request
- **Format**: Output format (wav/mp3/ogg)
- **Model**: Language model selection
- **Reference**: Voice cloning audio

## Troubleshooting

### Common Issues

#### 🔴 "CoquiTTS não está instalado"
**Solution**: Install TTS package
```bash
pip install TTS
```

#### 🔴 Model Not Found / Download Failed
**Solution**: The models are downloaded automatically. Ensure internet connection.

#### 🔴 Voice Cloning Not Working
**Cause**: Incorrect model or reference audio format
**Solution**: Use XTTS v2 or YourTTS models with WAV reference audio

#### 🔴 Unsupported Format
**Cause**: Missing FFmpeg or audio format issues
**Solution**: Install FFmpeg and ensure clean audio files

### Debug Information
Check these endpoints for troubleshooting:
- `GET /health` - Overall system health
- `GET /api/test/config` - Configuration check
- `POST /api/tts/generate` with debug logging

## Integration Notes

### ✅ What's Integrated:
- ✅ Complete TTS synthesis engine
- ✅ Voice cloning capabilities
- ✅ Profile management system
- ✅ Frontend interface (full tab)
- ✅ Backend API endpoints
- ✅ Auto-migration from legacy data

### 🔄 Future Enhancements:
- 🔄 Fine-tuning script integration
- 🔄 Bulk processing capabilities
- 🔄 Model export/import features
- 🔄 Advanced emotion control
- 🔄 Real-time synthesis improvements

## Usage Examples

### Basic TTS
```javascript
// Frontend call example
const response = await fetch('/api/tts/generate', {
  method: 'POST',
  body: new FormData({
    text: "Olá, mundo!",
    language: "tts_models/multilingual/multi-dataset/xtts_v2",
    format: "wav",
    device: "cpu"
  })
});
```

### Voice Cloning
```javascript
// With reference audio
const formData = new FormData();
formData.append('text', 'Texto a sintetizar');
formData.append('language', 'tts_models/multilingual/multi-dataset/xtts_v2');
formData.append('voice_sample', audioFile); // Reference .wav
```

## Performance Tips

1. **Model Selection**: XTTS v2 for quality, Tacotron2 for speed
2. **Text Length**: Keep under 500 characters for optimal performance
3. **Reference Audio**: Use 3-10 second clean WAV files for cloning
4. **Hardware**: GPU accelerates processing but isn't required
5. **Caching**: Profiles speed up repeated use with same voices

## Support and Resources

- 📖 **CoquiTTS Docs**: https://tts.readthedocs.io/
- 🎯 **Project**: coquittsbasic/ (reference implementation)
- 🔧 **Integration**: Fully integrated with main application
- 🎵 **Audio Quality**: Excellent with XTTS v2 model

---

**Status**: ✅ **FULLY INTEGRATED AND READY TO USE**
**Created**: TTS VoxClone tab successfully added to main application
**Compatibility**: Works with existing LLM and DB systems