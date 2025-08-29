#!/usr/bin/env python3
"""
Teste final sem MeCab
"""

import os

def test_tts_without_mecab():
    """Testa TTS sem MeCab"""
    print("🧪 TESTE FINAL SEM MECAB")
    print("=" * 50)
    
    # Configurar ambiente
    os.environ["COQUI_TOS_AGREED"] = "1"
    os.environ["PYTHONWARNINGS"] = "ignore"
    
    try:
        print("🔄 Importando TTS...")
        from TTS.api import TTS
        print("✅ TTS importado sem MeCab!")
        
        print("🔄 Carregando XTTS v2...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        print("✅ XTTS v2 carregado!")
        
        if hasattr(tts, 'tts_to_file'):
            print("✅ Método tts_to_file disponível")
            
            # Teste rápido de síntese
            print("🔄 Teste rápido de síntese...")
            
            import numpy as np
            import soundfile as sf
            
            # Criar referência
            duration = 1.0
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = 0.3 * np.sin(2 * np.pi * 440 * t)
            
            ref_path = "final_test_ref.wav"
            sf.write(ref_path, audio, sample_rate)
            
            # Síntese
            output_path = "final_test_output.wav"
            tts.tts_to_file(
                text="Final test without MeCab.",
                file_path=output_path,
                speaker_wav=ref_path,
                language="en"
            )
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ Síntese funcionou! {file_size} bytes")
                
                # Limpar
                os.remove(ref_path)
                os.remove(output_path)
                
                print("🎉 SUCESSO TOTAL!")
                print("✅ MeCab removido")
                print("✅ TTS funcionando")
                print("✅ XTTS v2 operacional")
                print("✅ Síntese de voz funcionando")
                
                return True
            else:
                print("❌ Arquivo não gerado")
                return False
        else:
            print("❌ Método tts_to_file não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_tts_without_mecab()
    
    if success:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("Execute: start_enhanced_correct.bat")
    else:
        print("\n❌ AINDA HÁ PROBLEMAS")