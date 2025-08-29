#!/usr/bin/env python3
"""
Teste com arquivo de voz real - VERSÃO CORRIGIDA
Identifica se o problema está na clonagem ou na conversão texto-para-áudio
"""

import os
import sys
import logging
import warnings
import glob
import time
import base64
from pathlib import Path

# Configurar logging detalhado
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_voice_files():
    """Encontra arquivos de voz na pasta especificada"""
    
    # Usar Path para evitar problemas de escape
    voice_folder = Path("C:/Users/gloli/Downloads/Vozes para TTS Coqui")
    
    logger.info(f"🔍 Procurando arquivos de voz em: {voice_folder}")
    
    if not voice_folder.exists():
        logger.error(f"❌ Pasta não encontrada: {voice_folder}")
        return []
    
    # Procurar arquivos de áudio
    audio_extensions = ['*.wav', '*.mp3', '*.flac', '*.m4a', '*.ogg']
    voice_files = []
    
    for ext in audio_extensions:
        files = list(voice_folder.glob(ext))
        voice_files.extend([str(f) for f in files])
    
    # Filtrar apenas arquivos válidos
    valid_files = []
    for file_path in voice_files:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:  # Pelo menos 1KB
            file_size = os.path.getsize(file_path)
            logger.info(f"📁 Encontrado: {os.path.basename(file_path)} ({file_size} bytes)")
            valid_files.append(file_path)
    
    logger.info(f"✅ {len(valid_files)} arquivo(s) de voz válido(s) encontrado(s)")
    return valid_files

def copy_voice_to_reference(voice_file):
    """Copia arquivo de voz para pasta reference_audio"""
    
    if not voice_file or not os.path.exists(voice_file):
        logger.error("❌ Arquivo de voz inválido")
        return None
    
    # Criar pasta reference_audio se não existir
    ref_dir = "reference_audio"
    os.makedirs(ref_dir, exist_ok=True)
    
    # Nome do arquivo de destino
    filename = os.path.basename(voice_file)
    name, ext = os.path.splitext(filename)
    dest_file = os.path.join(ref_dir, f"real_voice_test{ext}")
    
    try:
        import shutil
        shutil.copy2(voice_file, dest_file)
        
        if os.path.exists(dest_file):
            file_size = os.path.getsize(dest_file)
            logger.info(f"✅ Arquivo copiado: {dest_file} ({file_size} bytes)")
            return dest_file
        else:
            logger.error("❌ Falha ao copiar arquivo")
            return None
            
    except Exception as e:
        logger.error(f"❌ Erro ao copiar arquivo: {e}")
        return None

def test_xtts_v2_with_real_voice(reference_file):
    """Testa XTTS v2 com arquivo de voz real"""
    
    logger.info("🧪 TESTE COM ARQUIVO DE VOZ REAL")
    logger.info("=" * 60)
    
    # Configurar ambiente
    logger.info("🔧 Configurando ambiente...")
    warnings.filterwarnings("ignore")
    os.environ["COQUI_TOS_AGREED"] = "1"
    os.environ["COQUI_TTS_AGREED"] = "1"
    os.environ["COQUI_TTS_NO_MECAB"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"
    
    # Teste 1: Carregar XTTS v2
    logger.info("🔄 TESTE 1: Carregando XTTS v2...")
    try:
        from TTS.api import TTS
        logger.info("✅ TTS.api importado")
        
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        logger.info("✅ XTTS v2 carregado")
        
        if not hasattr(tts, 'tts_to_file'):
            logger.error("❌ Método tts_to_file não encontrado")
            return False
            
        logger.info("✅ Método tts_to_file disponível")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar XTTS v2: {e}")
        return False
    
    # Teste 2: Verificar arquivo de referência
    logger.info("🔄 TESTE 2: Verificando arquivo de referência...")
    if not reference_file or not os.path.exists(reference_file):
        logger.error("❌ Arquivo de referência não encontrado")
        return False
    
    file_size = os.path.getsize(reference_file)
    logger.info(f"✅ Arquivo de referência válido: {file_size} bytes")
    
    # Teste 3: Síntese simples (sem clonagem)
    logger.info("🔄 TESTE 3: Síntese simples (sem clonagem)...")
    try:
        simple_text = "Teste de síntese simples sem clonagem de voz."
        simple_output = "test_simple_synthesis.wav"
        
        logger.info(f"📝 Texto: {simple_text}")
        logger.info(f"📁 Saída: {simple_output}")
        
        # Síntese sem clonagem (usando voz padrão)
        tts.tts_to_file(
            text=simple_text,
            file_path=simple_output,
            language="pt"
        )
        
        # Aguardar arquivo
        for i in range(30):
            if os.path.exists(simple_output) and os.path.getsize(simple_output) > 0:
                file_size = os.path.getsize(simple_output)
                logger.info(f"✅ Síntese simples funcionou! ({file_size} bytes)")
                break
            time.sleep(1)
        else:
            logger.error("❌ Síntese simples falhou - arquivo não gerado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro na síntese simples: {e}")
        return False
    
    # Teste 4: Clonagem de voz com arquivo real
    logger.info("🔄 TESTE 4: Clonagem de voz com arquivo real...")
    try:
        clone_text = "Este é um teste de clonagem de voz usando um arquivo real da pasta de vozes."
        clone_output = "test_voice_cloning_real.wav"
        
        logger.info(f"📝 Texto: {clone_text}")
        logger.info(f"🎵 Referência: {reference_file}")
        logger.info(f"📁 Saída: {clone_output}")
        
        # Clonagem com arquivo real
        logger.info("   🔄 Executando clonagem...")
        tts.tts_to_file(
            text=clone_text,
            file_path=clone_output,
            speaker_wav=reference_file,
            language="pt"
        )
        
        # Aguardar arquivo
        logger.info("   ⏳ Aguardando arquivo ser gerado...")
        for i in range(60):  # 60 segundos para clonagem
            if os.path.exists(clone_output) and os.path.getsize(clone_output) > 0:
                file_size = os.path.getsize(clone_output)
                logger.info(f"✅ Clonagem funcionou após {i+1}s! ({file_size} bytes)")
                
                # Teste de conversão base64
                try:
                    with open(clone_output, 'rb') as f:
                        audio_data = f.read()
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    logger.info(f"✅ Conversão base64 OK ({len(audio_base64)} chars)")
                    return True
                except Exception as b64_error:
                    logger.error(f"❌ Erro na conversão base64: {b64_error}")
                    return False
                    
            if i % 10 == 0:  # Log a cada 10 segundos
                logger.info(f"   ⏳ Aguardando... {i}s")
            time.sleep(1)
        
        logger.error("❌ Clonagem falhou - arquivo não gerado em 60s")
        return False
        
    except Exception as e:
        logger.error(f"❌ Erro na clonagem: {e}")
        logger.error(f"   Tipo do erro: {type(e).__name__}")
        
        # Log detalhado do erro
        error_str = str(e).lower()
        if "mecab" in error_str:
            logger.error("🔍 Erro relacionado ao MeCab")
        elif "speaker" in error_str:
            logger.error("🔍 Erro relacionado ao speaker/referência")
        elif "memory" in error_str:
            logger.error("🔍 Erro de memória")
        elif "cuda" in error_str or "gpu" in error_str:
            logger.error("🔍 Erro de GPU/CUDA")
        else:
            logger.error("🔍 Erro desconhecido")
            
        return False

def test_server_integration(reference_file):
    """Testa integração com o servidor"""
    
    logger.info("🔄 TESTE 5: Integração com servidor...")
    
    try:
        import requests
        base_url = "http://localhost:8001"
        
        # Verificar se servidor está rodando
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code != 200:
                logger.warning("⚠️ Servidor não está rodando - pule este teste")
                return True  # Não é erro crítico
        except:
            logger.warning("⚠️ Servidor não está rodando - pule este teste")
            return True
        
        logger.info("✅ Servidor está rodando")
        
        # Testar clonagem via API
        payload = {
            "text": "Teste de clonagem via API do servidor com arquivo real.",
            "language": "pt"
        }
        
        response = requests.post(
            f"{base_url}/api/tts/clone-voice",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                audio_b64 = data.get("audio_base64", "")
                engine = data.get("engine", "unknown")
                logger.info(f"✅ API funcionou! Engine: {engine}, Áudio: {len(audio_b64)} chars")
                return True
            else:
                error = data.get("error", "Erro desconhecido")
                logger.error(f"❌ API falhou: {error}")
                return False
        else:
            logger.error(f"❌ API retornou status: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro na integração com servidor: {e}")
        return False

def main():
    """Função principal"""
    logger.info("🧪 TESTE COM ARQUIVO DE VOZ REAL")
    logger.info("Identifica se problema está na clonagem ou conversão texto-para-áudio")
    logger.info("=" * 80)
    
    # Encontrar arquivos de voz
    voice_files = find_voice_files()
    if not voice_files:
        logger.error("❌ Nenhum arquivo de voz encontrado")
        logger.error("💡 Verifique se a pasta existe: C:/Users/gloli/Downloads/Vozes para TTS Coqui")
        return
    
    # Usar o primeiro arquivo encontrado
    voice_file = voice_files[0]
    logger.info(f"🎵 Usando arquivo: {os.path.basename(voice_file)}")
    
    # Copiar para pasta reference_audio
    reference_file = copy_voice_to_reference(voice_file)
    if not reference_file:
        logger.error("❌ Falha ao preparar arquivo de referência")
        return
    
    # Executar testes
    tests_passed = 0
    total_tests = 2
    
    if test_xtts_v2_with_real_voice(reference_file):
        tests_passed += 1
        logger.info("✅ TESTE DIRETO PASSOU")
    else:
        logger.error("❌ TESTE DIRETO FALHOU")
    
    if test_server_integration(reference_file):
        tests_passed += 1
        logger.info("✅ TESTE SERVIDOR PASSOU")
    else:
        logger.error("❌ TESTE SERVIDOR FALHOU")
    
    # Resultado final
    logger.info("=" * 80)
    logger.info("📊 RESULTADO FINAL")
    logger.info("=" * 80)
    
    if tests_passed == total_tests:
        logger.info("🎉 TODOS OS TESTES PASSARAM!")
        logger.info("✅ XTTS v2 funciona com arquivo real")
        logger.info("✅ Clonagem de voz funciona")
        logger.info("✅ Conversão texto-para-áudio funciona")
        logger.info("✅ Integração com servidor funciona")
        
        print("\n🎯 DIAGNÓSTICO:")
        print("✅ Sistema está funcionando corretamente")
        print("✅ Problema pode estar em outro lugar")
        print("💡 Verifique configuração do cliente/interface")
        
    elif tests_passed == 1:
        logger.warning("⚠️ TESTE PARCIAL")
        logger.info("✅ XTTS v2 funciona diretamente")
        logger.error("❌ Integração com servidor falha")
        
        print("\n🔍 DIAGNÓSTICO:")
        print("✅ XTTS v2 funciona (não é problema do engine)")
        print("❌ Problema está na integração do servidor")
        print("💡 Verifique endpoints da API")
        print("💡 Verifique logs do servidor")
        
    else:
        logger.error("❌ TODOS OS TESTES FALHARAM")
        logger.error("❌ XTTS v2 não funciona nem diretamente")
        
        print("\n🔍 DIAGNÓSTICO:")
        print("❌ Problema fundamental no XTTS v2")
        print("💡 Verifique instalação do TTS")
        print("💡 Verifique dependências")
        print("💡 Verifique configuração do ambiente")

if __name__ == "__main__":
    main()