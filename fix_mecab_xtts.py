#!/usr/bin/env python3
"""
Correção do MeCab para XTTS v2 funcionar corretamente
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_mecab_configuration():
    """Corrige a configuração do MeCab para XTTS v2"""
    logger.info("🔧 Corrigindo configuração do MeCab...")
    
    try:
        # Método 1: Desabilitar MeCab completamente (mais seguro)
        logger.info("🔄 Desabilitando MeCab para evitar conflitos...")
        
        os.environ["COQUI_TTS_NO_MECAB"] = "1"
        os.environ["MECAB_PATH"] = ""
        os.environ["MECAB_CHARSET"] = ""
        os.environ["MECAB_DIC_PATH"] = ""
        
        # Configurações adicionais para desabilitar MeCab
        os.environ["DISABLE_MECAB"] = "1"
        os.environ["NO_MECAB"] = "1"
        
        logger.info("✅ MeCab desabilitado via variáveis de ambiente")
        
        # Método 2: Tentar configurar MeCab corretamente (fallback)
        mecab_dir = "C:\\mecab"
        if os.path.exists(mecab_dir):
            logger.info("🔄 Tentando configurar MeCab existente...")
            
            # Configurar caminhos do MeCab
            os.environ["MECAB_PATH"] = mecab_dir
            os.environ["MECAB_DIC_PATH"] = os.path.join(mecab_dir, "dic")
            os.environ["MECAB_RC"] = os.path.join(mecab_dir, "mecabrc")
            
            logger.info(f"📍 MECAB_PATH: {mecab_dir}")
            logger.info(f"📍 MECAB_DIC_PATH: {os.path.join(mecab_dir, 'dic')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar MeCab: {e}")
        return False

def test_xtts_without_mecab():
    """Testa XTTS v2 com MeCab desabilitado"""
    logger.info("🧪 Testando XTTS v2 com MeCab desabilitado...")
    
    try:
        # Configurar ambiente
        os.environ["COQUI_TOS_AGREED"] = "1"
        
        # Desabilitar MeCab completamente
        fix_mecab_configuration()
        
        # Suprimir warnings
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        
        # Importar TTS
        from TTS.api import TTS
        logger.info("✅ TTS.api importado com sucesso")
        
        # Tentar carregar XTTS v2
        logger.info("🔄 Carregando XTTS v2 sem MeCab...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        logger.info("✅ XTTS v2 carregado com sucesso!")
        
        # Verificar métodos
        if hasattr(tts, 'tts_to_file'):
            logger.info("✅ Método tts_to_file disponível")
            return tts
        else:
            logger.error("❌ Método tts_to_file não encontrado")
            return None
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar XTTS v2: {e}")
        return None

def test_simple_synthesis(tts_instance):
    """Testa síntese simples com XTTS v2"""
    logger.info("🔄 Testando síntese simples...")
    
    try:
        # Criar áudio de referência dummy
        import numpy as np
        import soundfile as sf
        
        # Gerar áudio sintético
        duration = 2.0
        sample_rate = 22050
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.3 * np.sin(2 * np.pi * 440 * t)
        
        # Salvar como referência
        ref_path = "test_reference.wav"
        sf.write(ref_path, audio, sample_rate)
        
        if not os.path.exists(ref_path):
            logger.error("❌ Não foi possível criar áudio de referência")
            return False
        
        logger.info(f"✅ Áudio de referência criado: {ref_path}")
        
        # Testar síntese
        output_path = "test_output_mecab_fix.wav"
        
        tts_instance.tts_to_file(
            text="Testing XTTS version 2 without MeCab conflicts.",
            file_path=output_path,
            speaker_wav=ref_path,
            language="en"
        )
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            logger.info(f"✅ Síntese funcionou: {output_path} ({file_size} bytes)")
            
            # Limpar arquivos de teste
            os.remove(ref_path)
            os.remove(output_path)
            
            return True
        else:
            logger.error("❌ Arquivo de saída não foi gerado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro na síntese: {e}")
        return False

def create_mecab_fix_script():
    """Cria script para aplicar correção do MeCab"""
    logger.info("📝 Criando script de correção do MeCab...")
    
    script_content = '''
def apply_mecab_fix():
    """Aplica correção do MeCab no main_enhanced.py"""
    import os
    import warnings
    
    # Desabilitar MeCab completamente
    os.environ["COQUI_TTS_NO_MECAB"] = "1"
    os.environ["MECAB_PATH"] = ""
    os.environ["MECAB_CHARSET"] = ""
    os.environ["MECAB_DIC_PATH"] = ""
    os.environ["DISABLE_MECAB"] = "1"
    os.environ["NO_MECAB"] = "1"
    
    # Suprimir warnings do MeCab
    warnings.filterwarnings("ignore", message=".*MeCab.*")
    warnings.filterwarnings("ignore", message=".*mecab.*")
    
    return True

def load_xtts_v2_without_mecab():
    """Carrega XTTS v2 com MeCab desabilitado"""
    try:
        # Aplicar correção do MeCab
        apply_mecab_fix()
        
        # Configurar ambiente
        import os
        import warnings
        import platform
        
        warnings.filterwarnings("ignore")
        os.environ["COQUI_TOS_AGREED"] = "1"
        
        if platform.system() == "Windows":
            os.environ["COQUI_TTS_NO_MECAB"] = "1"
            os.environ["PYTHONIOENCODING"] = "utf-8"
        
        # Importar TTS API
        from TTS.api import TTS
        
        # Inicializar XTTS v2
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        
        return tts
        
    except Exception as e:
        print(f"Erro ao carregar XTTS v2: {e}")
        return None
'''
    
    with open("mecab_fix_implementation.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    logger.info("✅ Script de correção criado: mecab_fix_implementation.py")

def main():
    """Função principal"""
    print("🔧 CORREÇÃO DO MECAB PARA XTTS v2")
    print("Resolvendo conflitos do MeCab no Windows")
    print("=" * 60)
    
    # 1. Corrigir configuração do MeCab
    mecab_ok = fix_mecab_configuration()
    if not mecab_ok:
        print("❌ Falha ao configurar MeCab")
        return False
    
    # 2. Testar XTTS v2 sem MeCab
    tts_instance = test_xtts_without_mecab()
    if not tts_instance:
        print("❌ XTTS v2 não carregou mesmo com correção do MeCab")
        return False
    
    # 3. Testar síntese simples
    synthesis_ok = test_simple_synthesis(tts_instance)
    if not synthesis_ok:
        print("❌ Síntese não funcionou")
        return False
    
    # 4. Criar script de correção
    create_mecab_fix_script()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    print("🎉 CORREÇÃO DO MECAB APLICADA COM SUCESSO!")
    print("✅ MeCab desabilitado para evitar conflitos")
    print("✅ XTTS v2 carregando corretamente")
    print("✅ Síntese funcionando perfeitamente")
    print("✅ Script de correção criado")
    
    print("\n🔧 CORREÇÕES APLICADAS:")
    print("• MeCab completamente desabilitado via variáveis de ambiente")
    print("• XTTS v2 funcionando sem dependência do MeCab")
    print("• Warnings do MeCab suprimidos")
    print("• Configuração robusta para Windows")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Integrar correção no main_enhanced.py")
    print("2. Reiniciar servidor com venv ativo")
    print("3. Testar clonagem na interface")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 CORREÇÃO DO MECAB CONCLUÍDA COM SUCESSO!")
    else:
        print("\n❌ CORREÇÃO FALHOU - VERIFIQUE OS ERROS ACIMA")