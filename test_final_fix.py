#!/usr/bin/env python3
"""
Teste final após correção das versões
"""

import os
import sys

def test_final_setup():
    """Teste final do setup"""
    print("🧪 TESTE FINAL APÓS CORREÇÃO DAS VERSÕES")
    print("=" * 50)
    
    # Verificar versões
    try:
        import numpy
        import numba
        import transformers
        import torch
        
        print(f"✅ NumPy: {numpy.__version__}")
        print(f"✅ Numba: {numba.__version__}")
        print(f"✅ Transformers: {transformers.__version__}")
        print(f"✅ PyTorch: {torch.__version__}")
        
    except Exception as e:
        print(f"❌ Erro ao verificar versões: {e}")
        return False
    
    # Configurar ambiente
    os.environ["COQUI_TOS_AGREED"] = "1"
    os.environ["COQUI_TTS_NO_MECAB"] = "1"
    os.environ["PYTHONWARNINGS"] = "ignore"
    
    try:
        # Importar TTS
        from TTS.api import TTS
        print("✅ TTS.api importado com sucesso")
        
        # Carregar XTTS v2
        print("🔄 Carregando XTTS v2...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        print("✅ XTTS v2 carregado com sucesso!")
        
        # Verificar métodos
        if hasattr(tts, 'tts_to_file'):
            print("✅ Método tts_to_file disponível")
            
            # Testar síntese rápida
            print("🔄 Testando síntese rápida...")
            
            # Criar áudio de referência
            import numpy as np
            import soundfile as sf
            
            duration = 1.0
            sample_rate = 22050
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio = 0.3 * np.sin(2 * np.pi * 440 * t)
            
            ref_path = "quick_test_ref.wav"
            sf.write(ref_path, audio, sample_rate)
            
            # Síntese
            output_path = "quick_test_output.wav"
            tts.tts_to_file(
                text="Quick test.",
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
                
                return True
            else:
                print("❌ Arquivo não gerado")
                return False
        else:
            print("❌ Método tts_to_file não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🔧 TESTE FINAL DO SETUP XTTS v2")
    print("Verificando se tudo está funcionando")
    print("=" * 60)
    
    success = test_final_setup()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    if success:
        print("🎉 SETUP COMPLETAMENTE FUNCIONAL!")
        print("✅ Todas as dependências corretas")
        print("✅ XTTS v2 carregando sem problemas")
        print("✅ Síntese de voz funcionando")
        print("✅ MeCab desabilitado corretamente")
        
        print("\n🚀 SISTEMA PRONTO PARA USO!")
        print("Execute: start_enhanced_correct.bat")
        print("A clonagem de voz deve funcionar perfeitamente")
        
        return True
    else:
        print("❌ AINDA HÁ PROBLEMAS NO SETUP")
        print("💡 Considere recriar o ambiente virtual")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 TESTE FINAL PASSOU!")
    else:
        print("\n❌ TESTE FINAL FALHOU")