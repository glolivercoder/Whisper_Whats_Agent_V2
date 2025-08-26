#!/usr/bin/env python3
"""
Minimal test to load Coqui TTS Portuguese model directly
"""

import os
import sys

# Set environment variables to fix MeCab issues on Windows
os.environ['MECAB_PATH'] = ''
os.environ['MECAB_CHARSET'] = 'utf8'
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['COQUI_TTS_NO_MECAB'] = '1'

print("🔧 Environment variables set for Coqui TTS on Windows")

# Add the CoquiTTS directory to the path
coqui_dir = os.path.join(os.path.dirname(__file__))
project_root = os.path.dirname(coqui_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    print("\n🔄 Importing TTS components...")
    
    # Import the model manager directly
    from TTS.utils.manage import ModelManager
    from TTS.utils.synthesizer import Synthesizer
    from TTS.config import load_config
    
    print("✅ TTS components imported successfully")
    
    # Initialize model manager
    manager = ModelManager()
    
    # Download/get the Portuguese model
    model_name = "tts_models/pt/cv/vits"
    print(f"\n🔄 Getting model path for {model_name}...")
    
    model_path, config_path, vocoder_path, vocoder_config_path, model_dir = manager.download_model(model_name)
    print(f"✅ Model paths obtained")
    print(f"   Model path: {model_path}")
    print(f"   Config path: {config_path}")
    
    # Load config
    print("\n🔄 Loading model config...")
    config = load_config(config_path)
    print("✅ Model config loaded")
    
    # Initialize synthesizer directly
    print("\n🔄 Initializing synthesizer...")
    synthesizer = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        vocoder_checkpoint=vocoder_path,
        vocoder_config=vocoder_config_path,
        use_cuda=False
    )
    print("✅ Synthesizer initialized")
    
    # Test synthesis
    print("\n🔄 Testing speech synthesis...")
    wav = synthesizer.tts("Olá, este é um teste de voz.")
    print("✅ Speech synthesis completed")
    
    # Save to file
    print("\n🔄 Saving to file...")
    synthesizer.save_wav(wav, "test_output.wav")
    print("✅ Audio saved to test_output.wav")
    
    print("\n🎉 Coqui TTS is working correctly with Portuguese model!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n📋 Test completed successfully!")