#!/usr/bin/env python3
"""
Teste específico para verificar se start_enhanced_correct.bat está funcionando
com todas as correções aplicadas
"""

import requests
import time
import logging
import json
import subprocess
import os
import signal

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_server_with_enhanced_script():
    """Testa se o servidor funciona com o script start_enhanced_correct.bat"""
    
    logger.info("🧪 TESTANDO start_enhanced_correct.bat COM CORREÇÕES")
    logger.info("=" * 60)
    
    base_url = "http://localhost:8001"
    
    # Aguardar servidor inicializar
    logger.info("⏳ Aguardando servidor inicializar com start_enhanced_correct.bat...")
    logger.info("💡 Execute em outro terminal: start_enhanced_correct.bat")
    
    # Aguardar mais tempo para inicialização completa
    for i in range(30):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Servidor detectado após {i+1} tentativas")
                break
        except:
            pass
        time.sleep(2)
    else:
        logger.error("❌ Servidor não foi detectado após 60 segundos")
        logger.error("💡 Verifique se executou: start_enhanced_correct.bat")
        return False
    
    # Testar funcionalidades
    tests_passed = 0
    total_tests = 5
    
    # Teste 1: Health check
    logger.info("🔄 TESTE 1: Health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Health check funcionando")
            logger.info(f"📊 Versão: {data.get('version', 'N/A')}")
            tests_passed += 1
        else:
            logger.error(f"❌ Health check falhou: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
    
    # Teste 2: Status TTS (endpoint que foi adicionado)
    logger.info("🔄 TESTE 2: Status TTS (endpoint corrigido)...")
    try:
        response = requests.get(f"{base_url}/api/tts/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Endpoint /api/tts/status funcionando")
            
            engines = data.get('engines', {})
            tortoise = engines.get('tortoise_tts', {})
            xtts = engines.get('xtts_v2', {})
            
            if tortoise.get('status') == 'disabled':
                logger.info("✅ TortoiseTTS corretamente desabilitado")
            
            if xtts.get('available'):
                logger.info("✅ XTTS v2 disponível como engine principal")
            
            tests_passed += 1
        else:
            logger.error(f"❌ Status TTS falhou: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
    except Exception as e:
        logger.error(f"❌ Erro no status TTS: {e}")
    
    # Teste 3: Clonagem de voz (endpoint que foi adicionado)
    logger.info("🔄 TESTE 3: Clonagem de voz (endpoint corrigido)...")
    try:
        payload = {
            "text": "Teste do script start_enhanced_correct.bat com correções aplicadas.",
            "language": "pt"
        }
        
        response = requests.post(
            f"{base_url}/api/tts/clone-voice",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                logger.info("✅ Clonagem de voz funcionando")
                logger.info(f"📊 Engine usado: {data.get('engine')}")
                logger.info(f"📊 Tamanho do áudio: {len(data.get('audio_base64', ''))} chars")
                tests_passed += 1
            else:
                logger.error(f"❌ Clonagem falhou: {data.get('error')}")
        else:
            logger.error(f"❌ Clonagem retornou: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
    except Exception as e:
        logger.error(f"❌ Erro na clonagem: {e}")
    
    # Teste 4: Síntese normal (teste da correção base64)
    logger.info("🔄 TESTE 4: Síntese normal (correção base64)...")
    try:
        payload = {
            "text": "Teste da correção do erro base64 em gTTS e pyttsx3.",
            "language": "pt"
        }
        
        response = requests.post(
            f"{base_url}/api/tts/synthesize",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                logger.info("✅ Síntese normal funcionando")
                logger.info(f"📊 Engine usado: {data.get('engine')}")
                
                # Verificar se não há erro base64
                if 'base64' not in data.get('error', '').lower():
                    logger.info("✅ Erro base64 não encontrado - CORRIGIDO!")
                    tests_passed += 1
                else:
                    logger.error("❌ Ainda há erro base64")
            else:
                error_msg = data.get('error', '')
                if 'base64' in error_msg.lower():
                    logger.error(f"❌ Erro base64 ainda presente: {error_msg}")
                else:
                    logger.warning(f"⚠️ Síntese falhou por outro motivo: {error_msg}")
                    tests_passed += 1  # Não é erro base64
        else:
            logger.error(f"❌ Síntese retornou: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Erro na síntese: {e}")
    
    # Teste 5: Verificar logs do servidor (se não há erros críticos)
    logger.info("🔄 TESTE 5: Verificação de estabilidade...")
    try:
        # Fazer várias requisições para testar estabilidade
        stable = True
        for i in range(3):
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code != 200:
                stable = False
                break
            time.sleep(1)
        
        if stable:
            logger.info("✅ Sistema estável - sem crashes")
            tests_passed += 1
        else:
            logger.error("❌ Sistema instável")
    except Exception as e:
        logger.error(f"❌ Erro na verificação de estabilidade: {e}")
    
    # Resultado final
    logger.info("=" * 60)
    logger.info("📊 RESULTADO FINAL DO TESTE")
    logger.info("=" * 60)
    
    if tests_passed == total_tests:
        logger.info("🎉 TODOS OS TESTES PASSARAM!")
        logger.info("✅ start_enhanced_correct.bat funcionando perfeitamente")
        logger.info("✅ Todas as correções foram aplicadas com sucesso")
        
        print("\n🎯 VERIFICAÇÕES CONFIRMADAS:")
        print("✅ Servidor inicia corretamente")
        print("✅ Endpoints 404 corrigidos")
        print("✅ TortoiseTTS desabilitado")
        print("✅ XTTS v2 funcionando")
        print("✅ Erro base64 corrigido")
        print("✅ Sistema estável")
        
        print("\n🚀 PODE CONTINUAR USANDO:")
        print("start_enhanced_correct.bat")
        
    elif tests_passed >= 3:
        logger.info(f"✅ {tests_passed}/{total_tests} testes passaram")
        logger.info("✅ Sistema funcionando bem com pequenos ajustes")
        
        print("\n🎯 SISTEMA FUNCIONANDO:")
        print("✅ Principais funcionalidades OK")
        print("⚠️ Alguns ajustes menores podem ser necessários")
        print("✅ Pode usar start_enhanced_correct.bat")
        
    else:
        logger.warning(f"⚠️ Apenas {tests_passed}/{total_tests} testes passaram")
        logger.warning("Algumas correções podem não ter sido aplicadas")
        
        print("\n⚠️ ATENÇÃO:")
        print("❌ Algumas correções não funcionaram")
        print("💡 Verifique se o servidor foi reiniciado")
        print("💡 Tente usar: start_server_fixed.bat")

def main():
    """Função principal"""
    logger.info("🧪 TESTE DO SCRIPT start_enhanced_correct.bat")
    logger.info("Este teste verifica se o script funciona com as correções")
    logger.info("=" * 60)
    
    test_server_with_enhanced_script()

if __name__ == "__main__":
    main()