#!/usr/bin/env python3
"""
Corrige versões das dependências para compatibilidade com XTTS v2
"""

import subprocess
import sys
import os

def install_compatible_versions():
    """Instala versões compatíveis das dependências"""
    print("🔧 CORRIGINDO VERSÕES DAS DEPENDÊNCIAS")
    print("=" * 50)
    
    # Versões compatíveis baseadas nos erros encontrados
    compatible_packages = [
        "transformers==4.31.0",  # Versão específica para XTTS v2
        "tokenizers==0.13.3",    # Versão compatível
        "torch==2.4.1",
        "torchaudio==2.4.1"
    ]
    
    for package in compatible_packages:
        try:
            print(f"🔄 Instalando {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--force-reinstall"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} instalado com sucesso")
            else:
                print(f"⚠️ Problema ao instalar {package}: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Erro ao instalar {package}: {e}")
    
    print("✅ Instalação de versões compatíveis concluída")

def test_fixed_versions():
    """Testa se as versões corrigidas funcionam"""
    print("\n🧪 TESTANDO VERSÕES CORRIGIDAS")
    print("=" * 50)
    
    try:
        # Configurar ambiente
        os.environ["COQUI_TOS_AGREED"] = "1"
        os.environ["COQUI_TTS_NO_MECAB"] = "1"
        os.environ["PYTHONWARNINGS"] = "ignore"
        
        # Importar TTS
        from TTS.api import TTS
        print("✅ TTS.api importado")
        
        # Carregar XTTS v2
        print("🔄 Carregando XTTS v2...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        print("✅ XTTS v2 carregado")
        
        # Criar áudio de referência
        import numpy as np
        import soundfile as sf
        
        duration = 2.0
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.3 * np.sin(2 * np.pi * 440 * t)
        
        ref_path = "test_ref_fixed.wav"
        sf.write(ref_path, audio, sample_rate)
        print("✅ Áudio de referência criado")
        
        # Testar síntese
        output_path = "test_output_fixed.wav"
        
        print("🔄 Testando síntese...")
        tts.tts_to_file(
            text="Testing XTTS version 2 with fixed dependencies.",
            file_path=output_path,
            speaker_wav=ref_path,
            language="en"
        )
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Síntese funcionou! {file_size} bytes")
            
            # Limpar arquivos
            os.remove(ref_path)
            os.remove(output_path)
            
            return True
        else:
            print("❌ Arquivo não foi gerado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 CORREÇÃO DE VERSÕES PARA XTTS v2")
    print("Instalando versões compatíveis das dependências")
    print("=" * 60)
    
    # 1. Instalar versões compatíveis
    install_compatible_versions()
    
    # 2. Testar versões corrigidas
    test_ok = test_fixed_versions()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    if test_ok:
        print("🎉 VERSÕES CORRIGIDAS COM SUCESSO!")
        print("✅ Dependências compatíveis instaladas")
        print("✅ XTTS v2 funcionando corretamente")
        print("✅ Síntese de voz operacional")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Execute o servidor no ambiente virtual")
        print("2. Teste a clonagem de voz")
        print("3. Sistema deve funcionar sem erros")
        
        return True
    else:
        print("❌ AINDA HÁ PROBLEMAS COM AS VERSÕES")
        print("💡 Pode ser necessário reinstalar o ambiente virtual")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 CORREÇÃO DE VERSÕES CONCLUÍDA!")
    else:
        print("\n❌ CORREÇÃO FALHOU - CONSIDERE RECRIAR O VENV")