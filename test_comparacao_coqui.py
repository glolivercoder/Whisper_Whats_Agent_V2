#!/usr/bin/env python3
"""
Teste Comparativo: Aplicação Funcional vs Aplicação Atual
Testa as correções aplicadas baseadas na aplicação funcional
"""

import os
import sys
import tempfile
from datetime import datetime

def test_coqui_license_config():
    """Testa se a configuração da licença foi aplicada"""
    print("🔍 Testando configuração da licença...")
    
    # Verificar se as variáveis de ambiente foram definidas
    tos_agreed = os.environ.get("COQUI_TOS_AGREED")
    tts_agreed = os.environ.get("COQUI_TTS_AGREED")
    
    if tos_agreed == "1" or tts_agreed == "1":
        print("✅ Configuração da licença Coqui TTS detectada")
        return True
    else:
        print("❌ Configuração da licença Coqui TTS não encontrada")
        return False

def test_coqui_tts_import():
    """Testa se o Coqui TTS pode ser importado"""
    print("🔍 Testando importação do Coqui TTS...")
    
    try:
        from TTS.api import TTS
        print("✅ Coqui TTS importado com sucesso")
        return True
    except ImportError as e:
        print(f"❌ Erro na importação do Coqui TTS: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Erro inesperado na importação: {e}")
        return False

def test_xtts_v2_model():
    """Testa o carregamento do modelo XTTS v2"""
    print("🔍 Testando carregamento do modelo XTTS v2...")
    
    try:
        from TTS.api import TTS
        
        # Tentar carregar XTTS v2
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
        
        print("✅ Modelo XTTS v2 carregado com sucesso")
        return tts
        
    except Exception as e:
        print(f"❌ Erro no carregamento do XTTS v2: {e}")
        return None

def test_voice_cloning_parameters():
    """Testa os parâmetros de clonagem de voz"""
    print("🔍 Testando parâmetros de clonagem de voz...")
    
    tts = test_xtts_v2_model()
    if not tts:
        return False
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        # Criar um áudio de referência temporário
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as ref_file:
            ref_path = ref_file.name
        
        # Gerar áudio de referência
        tts.tts_to_file(
            text="Este é um áudio de referência para teste.",
            file_path=ref_path,
            language="pt"
        )
        
        # Testar clonagem com speaker_wav como lista (correção aplicada)
        tts.tts_to_file(
            text="Esta é uma voz clonada para teste.",
            file_path=temp_path,
            speaker_wav=[ref_path],  # LISTA - correção da aplicação funcional
            language="pt"
        )
        
        # Verificar se o arquivo foi criado
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            print("✅ Clonagem de voz funcionando com speaker_wav como lista")
            
            # Limpeza
            os.unlink(temp_path)
            os.unlink(ref_path)
            return True
        else:
            print("❌ Arquivo de áudio não foi gerado")
            return False
            
    except Exception as e:
        print(f"❌ Erro na clonagem de voz: {e}")
        return False

def run_comparative_tests():
    """Executa todos os testes comparativos"""
    print("🧪 EXECUTANDO TESTES COMPARATIVOS")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    tests = [
        ("Configuração da Licença", test_coqui_license_config),
        ("Importação do Coqui TTS", test_coqui_tts_import),
        ("Carregamento XTTS v2", lambda: test_xtts_v2_model() is not None),
        ("Parâmetros de Clonagem", test_voice_cloning_parameters)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🔄 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"   {status}")
        except Exception as e:
            results.append((test_name, False))
            print(f"   ❌ ERRO: {e}")
        print()
    
    # Resumo dos resultados
    print("📊 RESUMO DOS TESTES")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! As correções foram aplicadas com sucesso.")
    else:
        print("⚠️ Alguns testes falharam. Verifique os logs acima para mais detalhes.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comparative_tests()
    sys.exit(0 if success else 1)
