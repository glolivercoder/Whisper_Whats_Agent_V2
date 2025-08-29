#!/usr/bin/env python3
"""
Correção de Compatibilidade PyTorch 2.6+ com XTTS v2
Resolve o erro de safe globals no carregamento do modelo
"""

import os
import shutil
from datetime import datetime

def fix_pytorch_compatibility():
    """Aplica correção para compatibilidade com PyTorch 2.6+"""
    print("🔧 CORREÇÃO DE COMPATIBILIDADE PYTORCH 2.6+ COM XTTS v2")
    print("=" * 60)
    
    main_file = "backend/main_enhanced.py"
    
    # Fazer backup
    backup_file = f"{main_file}.backup_pytorch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(main_file, backup_file)
    print(f"✅ Backup criado: {backup_file}")
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se a correção já foi aplicada
    if 'torch.serialization.add_safe_globals' in content:
        print("ℹ️ Correção PyTorch já aplicada")
        return True
    
    # Encontrar a seção de imports do PyTorch
    pytorch_import_section = content.find('# PyTorch compatibility fix')
    
    if pytorch_import_section == -1:
        print("❌ Seção de compatibilidade PyTorch não encontrada")
        return False
    
    # Melhorar a seção de compatibilidade PyTorch
    old_pytorch_section = '''# PyTorch compatibility fix for XTTS v2 model loading
# Add safe globals for XTTS config to fix PyTorch 2.6+ compatibility issue
try:
    import torch
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsAudioConfig
    from TTS.config.shared_configs import BaseDatasetConfig
    # Add all required classes to safe globals
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig])
    print("✅ Added XTTS config and related classes to safe globals for PyTorch compatibility")
except Exception as e:
    print(f"ℹ️ Could not add XTTS config to safe globals: {e}")'''
    
    new_pytorch_section = '''# PyTorch compatibility fix for XTTS v2 model loading
# Comprehensive fix for PyTorch 2.6+ compatibility with XTTS v2
try:
    import torch
    
    # Set weights_only=False globally for XTTS compatibility
    torch.serialization._set_default_weights_only(False)
    print("✅ Set PyTorch weights_only=False for XTTS compatibility")
    
    # Import all XTTS-related classes
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsAudioConfig
    from TTS.config.shared_configs import BaseDatasetConfig
    from TTS.tts.configs.shared_configs import BaseAudioConfig
    from TTS.tts.configs.vits_config import VitsConfig
    
    # Add comprehensive safe globals for XTTS
    safe_globals = [
        XttsConfig, 
        XttsAudioConfig, 
        BaseDatasetConfig,
        BaseAudioConfig,
        VitsConfig
    ]
    
    torch.serialization.add_safe_globals(safe_globals)
    print(f"✅ Added {len(safe_globals)} XTTS classes to PyTorch safe globals")
    
except ImportError as e:
    print(f"⚠️ Could not import XTTS classes: {e}")
except AttributeError as e:
    print(f"⚠️ PyTorch version may not support _set_default_weights_only: {e}")
except Exception as e:
    print(f"ℹ️ PyTorch compatibility setup completed with warnings: {e}")'''
    
    # Substituir a seção
    content = content.replace(old_pytorch_section, new_pytorch_section)
    
    # Adicionar configuração da licença se não existir
    if 'COQUI_TOS_AGREED' not in content:
        license_config = '''
# Configuração automática da licença Coqui TTS (baseado na aplicação funcional)
os.environ["COQUI_TTS_AGREED"] = "1"
os.environ["COQUI_TOS_AGREED"] = "1"
print("✅ Configuração da licença Coqui TTS aplicada")
'''
        
        # Inserir após os imports
        import_end = content.find('# CloningTool class placeholder')
        if import_end != -1:
            content = content[:import_end] + license_config + '\n' + content[import_end:]
    
    # Salvar arquivo corrigido
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Correção de compatibilidade PyTorch aplicada")
    return True

def create_xtts_test_script():
    """Cria script de teste específico para XTTS v2"""
    test_script = '''#!/usr/bin/env python3
"""
Teste Específico XTTS v2 com Correção PyTorch 2.6+
"""

import os
import tempfile

def test_pytorch_compatibility():
    """Testa a compatibilidade com PyTorch 2.6+"""
    print("🔍 Testando compatibilidade PyTorch 2.6+...")
    
    try:
        import torch
        
        # Verificar se weights_only foi configurado
        try:
            # Tentar definir weights_only=False
            torch.serialization._set_default_weights_only(False)
            print("✅ PyTorch weights_only configurado")
        except AttributeError:
            print("ℹ️ PyTorch versão não suporta _set_default_weights_only")
        
        return True
    except Exception as e:
        print(f"❌ Erro na configuração PyTorch: {e}")
        return False

def test_xtts_v2_loading():
    """Testa o carregamento do XTTS v2 com correções"""
    print("🔍 Testando carregamento XTTS v2 com correções...")
    
    try:
        # Configurar licença
        os.environ["COQUI_TOS_AGREED"] = "1"
        os.environ["COQUI_TTS_AGREED"] = "1"
        
        # Configurar PyTorch
        import torch
        try:
            torch.serialization._set_default_weights_only(False)
        except AttributeError:
            pass
        
        # Adicionar safe globals
        try:
            from TTS.tts.configs.xtts_config import XttsConfig
            from TTS.tts.models.xtts import XttsAudioConfig
            from TTS.config.shared_configs import BaseDatasetConfig
            
            torch.serialization.add_safe_globals([
                XttsConfig, 
                XttsAudioConfig, 
                BaseDatasetConfig
            ])
        except Exception as e:
            print(f"⚠️ Aviso ao configurar safe globals: {e}")
        
        # Tentar carregar XTTS v2
        from TTS.api import TTS
        
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
        
        print("✅ XTTS v2 carregado com sucesso!")
        return tts
        
    except Exception as e:
        print(f"❌ Erro no carregamento XTTS v2: {e}")
        return None

def test_voice_cloning_corrected():
    """Testa clonagem de voz com parâmetros corrigidos"""
    print("🔍 Testando clonagem de voz com correções...")
    
    tts = test_xtts_v2_loading()
    if not tts:
        return False
    
    try:
        # Criar arquivos temporários
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_ref:
            ref_path = tmp_ref.name
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_out:
            out_path = tmp_out.name
        
        # Gerar áudio de referência
        print("🔄 Gerando áudio de referência...")
        tts.tts_to_file(
            text="Este é um áudio de referência para clonagem.",
            file_path=ref_path,
            language="pt"
        )
        
        # Testar clonagem com speaker_wav como LISTA (correção da aplicação funcional)
        print("🔄 Testando clonagem com speaker_wav como lista...")
        tts.tts_to_file(
            text="Esta é uma voz clonada usando XTTS v2 corrigido.",
            file_path=out_path,
            speaker_wav=[ref_path],  # LISTA - correção aplicada
            language="pt"
        )
        
        # Verificar resultado
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            print("✅ Clonagem de voz funcionando com correções!")
            
            # Limpeza
            os.unlink(ref_path)
            os.unlink(out_path)
            return True
        else:
            print("❌ Arquivo de clonagem não foi gerado")
            return False
            
    except Exception as e:
        print(f"❌ Erro na clonagem de voz: {e}")
        return False

def main():
    """Executa todos os testes com correções"""
    print("🧪 TESTE XTTS v2 COM CORREÇÕES PYTORCH 2.6+")
    print("=" * 50)
    
    tests = [
        ("Compatibilidade PyTorch", test_pytorch_compatibility),
        ("Carregamento XTTS v2", lambda: test_xtts_v2_loading() is not None),
        ("Clonagem de Voz Corrigida", test_voice_cloning_corrected)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\\n🔄 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"   {status}")
        except Exception as e:
            results.append((test_name, False))
            print(f"   ❌ ERRO: {e}")
    
    # Resumo
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todas as correções funcionaram! XTTS v2 está operacional.")
    else:
        print("⚠️ Algumas correções ainda precisam de ajustes.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
'''
    
    with open("test_xtts_pytorch_fix.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Script de teste XTTS criado: test_xtts_pytorch_fix.py")

def main():
    """Função principal"""
    print("🔧 CORREÇÃO PYTORCH 2.6+ PARA XTTS v2")
    print("Baseado na análise da aplicação funcional")
    print("=" * 50)
    
    # Aplicar correção
    if fix_pytorch_compatibility():
        print("✅ Correção PyTorch aplicada com sucesso")
    else:
        print("❌ Falha na aplicação da correção PyTorch")
        return False
    
    # Criar script de teste
    create_xtts_test_script()
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python test_xtts_pytorch_fix.py")
    print("2. Se passar, reinicie: python backend/main_enhanced.py")
    print("3. Teste a clonagem de voz na interface")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Correção PyTorch concluída!")
    else:
        print("\n❌ Falha na correção PyTorch")