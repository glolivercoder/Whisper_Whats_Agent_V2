#!/usr/bin/env python3
"""
Testa se as dependências foram instaladas corretamente no venv
"""

import sys
import os

def test_environment():
    """Testa o ambiente atual"""
    print("🔍 VERIFICANDO AMBIENTE VIRTUAL")
    print("=" * 50)
    
    # Verificar se está no venv
    python_path = sys.executable
    print(f"📍 Python path: {python_path}")
    
    is_venv = "venv" in python_path.lower()
    if is_venv:
        print("✅ Executando no ambiente virtual")
    else:
        print("❌ NÃO está no ambiente virtual!")
        print("💡 Execute: venv\\Scripts\\activate.bat")
        return False
    
    return True

def test_dependencies():
    """Testa as dependências críticas"""
    print("\n🔍 VERIFICANDO DEPENDÊNCIAS")
    print("=" * 50)
    
    dependencies = [
        ("torch", "2.4.1"),
        ("torchaudio", "2.4.1"),
        ("transformers", None),
        ("TTS", None),
        ("soundfile", None),
        ("librosa", None),
        ("numpy", None),
        ("scipy", None)
    ]
    
    all_ok = True
    
    for package, expected_version in dependencies:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'Unknown')
            
            if expected_version and version != expected_version:
                print(f"⚠️ {package}: {version} (esperado: {expected_version})")
            else:
                print(f"✅ {package}: {version}")
                
        except ImportError:
            print(f"❌ {package}: NÃO INSTALADO")
            all_ok = False
    
    return all_ok

def test_xtts_v2():
    """Testa se XTTS v2 carrega corretamente"""
    print("\n🧪 TESTANDO XTTS v2")
    print("=" * 50)
    
    try:
        # Configurar ambiente
        os.environ["COQUI_TOS_AGREED"] = "1"
        os.environ["COQUI_TTS_NO_MECAB"] = "1"
        
        # Importar TTS
        from TTS.api import TTS
        print("✅ TTS.api importado com sucesso")
        
        # Tentar carregar XTTS v2
        print("🔄 Carregando XTTS v2...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        print("✅ XTTS v2 carregado com sucesso!")
        
        # Verificar métodos
        if hasattr(tts, 'tts_to_file'):
            print("✅ Método tts_to_file disponível")
        else:
            print("❌ Método tts_to_file não encontrado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar XTTS v2: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 TESTE DE DEPENDÊNCIAS NO AMBIENTE VIRTUAL")
    print("Verificando se tudo foi instalado corretamente")
    print("=" * 60)
    
    # 1. Testar ambiente
    env_ok = test_environment()
    if not env_ok:
        return False
    
    # 2. Testar dependências
    deps_ok = test_dependencies()
    
    # 3. Testar XTTS v2
    xtts_ok = test_xtts_v2()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    if env_ok and deps_ok and xtts_ok:
        print("🎉 TUDO FUNCIONANDO PERFEITAMENTE!")
        print("✅ Ambiente virtual ativo")
        print("✅ Dependências instaladas")
        print("✅ XTTS v2 carregando corretamente")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Execute: start_enhanced_correct.bat")
        print("2. Teste a clonagem na interface")
        print("3. Não deve mais aparecer erros de dependências")
        
        return True
    else:
        print("❌ AINDA HÁ PROBLEMAS")
        
        if not env_ok:
            print("• Ative o ambiente virtual primeiro")
        if not deps_ok:
            print("• Algumas dependências estão faltando")
        if not xtts_ok:
            print("• XTTS v2 não está carregando corretamente")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("\n❌ TESTE FALHOU - VERIFIQUE OS PROBLEMAS ACIMA")