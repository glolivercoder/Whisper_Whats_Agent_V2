#!/usr/bin/env python3
"""
TESTE RÁPIDO DO SERVIDOR
========================

Testa rapidamente se o servidor está funcionando com os endpoints TTS.
"""

import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_endpoints():
    """Testa os endpoints principais"""
    base_url = "http://localhost:8001"
    
    tests = [
        ("Health Check", "GET", "/health"),
        ("TTS Status", "GET", "/api/tts/status"),
        ("API TTS", "POST", "/api/tts", {"text": "Teste rápido", "language": "pt"}),
    ]
    
    results = {}
    
    for test_name, method, endpoint, *payload in tests:
        try:
            logger.info(f"🔍 Testando: {test_name}")
            
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{base_url}{endpoint}", json=payload[0] if payload else {}, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ {test_name}: OK ({response.status_code})")
                results[test_name] = True
            else:
                logger.error(f"❌ {test_name}: FALHOU ({response.status_code})")
                results[test_name] = False
                
        except Exception as e:
            logger.error(f"❌ {test_name}: ERRO - {e}")
            results[test_name] = False
    
    # Resultado
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    logger.info("=" * 40)
    logger.info(f"📊 RESULTADO: {passed}/{total} testes passaram")
    
    for test_name, result in results.items():
        status = "✅ OK" if result else "❌ FALHOU"
        logger.info(f"   {test_name}: {status}")
    
    return passed == total

if __name__ == "__main__":
    logger.info("🧪 TESTE RÁPIDO DO SERVIDOR")
    logger.info("=" * 40)
    
    success = test_endpoints()
    
    if success:
        logger.info("🎉 SERVIDOR FUNCIONANDO PERFEITAMENTE!")
    else:
        logger.warning("⚠️ Alguns endpoints podem ter problemas")
    
    exit(0 if success else 1)