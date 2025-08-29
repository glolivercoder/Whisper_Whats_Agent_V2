#!/usr/bin/env python3
"""
Teste final para verificar se a correção do XTTS v2 funcionou
"""

import os
import sys
import logging
import warnings

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_xtts_v2_final_fix():
    """Testa se a correção final do XTTS v2 funcionou"""
    
    logger.info("🧪 TESTE FINAL DA CORREÇÃO XTTS v2")
    logger.info("=" * 50)
    
    # Configurar ambiente
    warnings.filterwarnings("ignore")
    os.environ["COQUI_TOS_AGREED"] = "1"
    os.environ["COQUI_TTS_AGREED"] = "1"
    os.environ["COQUI_TTS_NO_MECAB"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    
    # Carregar XTTS v2
    try:
        from TTS.api import TTS
        logger.info("✅ TTS.api importado")
        
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        logger.info("✅ XTTS v2 carregado")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar XTTS v2: {e}")
        return False
    
    # Verificar se arquivo dummy existe
    dummy_path = "reference_audio/dummy_reference.wav"
    if os.path.exists(dummy_path) and os.path.getsize(dummy_path) > 1000:
        logger.info(f"✅ Arquivo dummy existe: {dummy_path}")
    else:
        logger.error("❌ Arquivo dummy não existe ou é muito pequeno")
        return False
    
    # Teste de síntese com speaker_wav
    try:
        text = "Teste final da correção do XTTS versão 2 com speaker_wav obrigatório."
        output_path = "test_final_fix.wav"
        
        logger.info(f"🔄 Testando síntese...")
        logger.info(f"📝 Texto: {text}")
        logger.info(f"🎵 Speaker WAV: {dummy_path}")
        
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=dummy_path,
            language="pt"
        )
        
        # Verificar resultado
        import time
        for i in range(30):
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ Síntese funcionou! ({file_size} bytes)")
                
                # Testar conversão base64
                try:
                    import base64
                    with open(output_path, 'rb') as f:
                        audio_data = f.read()
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    logger.info(f"✅ Base64 OK ({len(audio_base64)} chars)")
                    return True
                except Exception as b64_error:
                    logger.error(f"❌ Erro base64: {b64_error}")
                    return False
                    
            time.sleep(1)
        
        logger.error("❌ Arquivo não foi gerado")
        return False
        
    except Exception as e:
        error_str = str(e).lower()
        if "invalid file" in error_str and "none" in error_str:
            logger.error("❌ ERRO AINDA PERSISTE: Invalid file: None")
            logger.error("💡 A correção não foi aplicada corretamente")
        else:
            logger.error(f"❌ Outro erro: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🔧 VERIFICAÇÃO FINAL DA CORREÇÃO XTTS v2")
    logger.info("=" * 60)
    
    if test_xtts_v2_final_fix():
        logger.info("=" * 60)
        logger.info("🎉 CORREÇÃO FUNCIONOU!")
        logger.info("✅ XTTS v2 funciona com speaker_wav")
        logger.info("✅ Erro 'Invalid file: None' foi eliminado")
        logger.info("✅ Sistema está pronto para uso")
        
        print("\n🎯 RESULTADO:")
        print("✅ Correção aplicada com sucesso")
        print("✅ XTTS v2 funcionando")
        print("✅ Áudio sendo gerado")
        print("✅ Base64 funcionando")
        
        print("\n🚀 PRÓXIMO PASSO:")
        print("Reinicie o servidor: start_enhanced_correct.bat")
        
    else:
        logger.error("=" * 60)
        logger.error("❌ CORREÇÃO NÃO FUNCIONOU")
        logger.error("❌ Erro ainda persiste")
        
        print("\n🔍 DIAGNÓSTICO:")
        print("❌ Correção não foi aplicada corretamente")
        print("💡 Verifique se o arquivo foi modificado")
        print("💡 Pode ser necessário aplicar correção manual")

if __name__ == "__main__":
    main()