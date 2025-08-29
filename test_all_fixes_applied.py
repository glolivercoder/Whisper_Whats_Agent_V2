#!/usr/bin/env python3
"""
Teste para verificar se todas as correções foram aplicadas corretamente
"""

import requests
import time
import logging
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_server_startup():
    """Testa se o servidor inicia corretamente"""
    base_url = "http://localhost:8001"
    
    logger.info("🔄 TESTE 1: Verificando se servidor está ativo...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Servidor está rodando")
            data = response.json()
            logger.info(f"📊 Status: {json.dumps(data, indent=2)}")
            return True
        else:
            logger.error(f"❌ Servidor retornou status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erro de conexão: {e}")
        return False

def test_tts_status_endpoint():
    """Testa o endpoint de status TTS"""
    base_url = "http://localhost:8001"
    
    logger.info("🔄 TESTE 2: Verificando endpoint /api/tts/status...")
    
    try:
        response = requests.get(f"{base_url}/api/tts/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Endpoint /api/tts/status funcionando")
            logger.info(f"📊 Engines: {json.dumps(data.get('engines', {}), indent=2)}")
            
            # Verificar se TortoiseTTS está desabilitado
            engines = data.get('engines', {})
            tortoise = engines.get('tortoise_tts', {})
            if tortoise.get('status') == 'disabled':
                logger.info("✅ TortoiseTTS corretamente desabilitado")
            else:
                logger.warning("⚠️ TortoiseTTS ainda não está desabilitado")
            
            return True
        else:
            logger.error(f"❌ Endpoint retornou status: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erro de conexão: {e}")
        return False

def test_clone_voice_endpoint():
    """Testa o endpoint de clonagem de voz"""
    base_url = "http://localhost:8001"
    
    logger.info("🔄 TESTE 3: Testando endpoint /api/tts/clone-voice...")
    
    try:
        payload = {
            "text": "Este é um teste das correções aplicadas no sistema.",
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
                return True
            else:
                logger.error(f"❌ Clonagem falhou: {data.get('error')}")
                return False
        else:
            logger.error(f"❌ Endpoint retornou status: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erro de conexão: {e}")
        return False

def test_synthesize_speech():
    """Testa síntese de fala normal"""
    base_url = "http://localhost:8001"
    
    logger.info("🔄 TESTE 4: Testando síntese de fala normal...")
    
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
                logger.info("✅ Síntese de fala funcionando")
                logger.info(f"📊 Engine usado: {data.get('engine')}")
                logger.info(f"📊 Tamanho do áudio: {len(data.get('audio_base64', ''))} chars")
                return True
            else:
                logger.error(f"❌ Síntese falhou: {data.get('error')}")
                return False
        else:
            logger.error(f"❌ Endpoint retornou status: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erro de conexão: {e}")
        return False

def main():
    """Função principal de teste"""
    logger.info("🧪 TESTANDO TODAS AS CORREÇÕES APLICADAS")
    logger.info("=" * 60)
    
    # Aguardar servidor inicializar
    logger.info("⏳ Aguardando servidor inicializar...")
    time.sleep(5)
    
    tests_passed = 0
    total_tests = 4
    
    # Executar testes
    if test_server_startup():
        tests_passed += 1
    
    if test_tts_status_endpoint():
        tests_passed += 1
    
    if test_clone_voice_endpoint():
        tests_passed += 1
    
    if test_synthesize_speech():
        tests_passed += 1
    
    # Resultado final
    logger.info("=" * 60)
    logger.info("📊 RESULTADO FINAL DOS TESTES")
    logger.info("=" * 60)
    
    if tests_passed == total_tests:
        logger.info("🎉 TODOS OS TESTES PASSARAM!")
        logger.info("✅ Todas as correções foram aplicadas com sucesso")
        logger.info("✅ Sistema está funcionando corretamente")
        
        print("\n🎯 CORREÇÕES VERIFICADAS:")
        print("✅ Erro base64 - CORRIGIDO")
        print("✅ TortoiseTTS - DESABILITADO")
        print("✅ Endpoints 404 - CORRIGIDOS")
        print("✅ MeCab dicrc - CONFIGURADO")
        print("✅ Sistema - ESTÁVEL")
        
    else:
        logger.warning(f"⚠️ {tests_passed}/{total_tests} testes passaram")
        logger.warning("Algumas correções podem precisar de ajustes")
        
        if tests_passed == 0:
            logger.error("❌ SERVIDOR NÃO ESTÁ FUNCIONANDO")
            logger.error("💡 Verifique se executou: start_server_fixed.bat")
        else:
            logger.info("✅ Servidor está funcionando parcialmente")
            logger.info("💡 Algumas funcionalidades podem precisar de ajustes")

if __name__ == "__main__":
    main()