#!/usr/bin/env python3
"""
Debug dos logs do servidor em tempo real
Monitora exatamente onde está falhando a geração de áudio
"""

import requests
import time
import logging
import json
import threading
import subprocess
import os
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ServerLogMonitor:
    """Monitor de logs do servidor em tempo real"""
    
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.monitoring = False
        
    def check_server_status(self):
        """Verifica status detalhado do servidor"""
        logger.info("🔍 VERIFICANDO STATUS DETALHADO DO SERVIDOR")
        logger.info("=" * 60)
        
        try:
            # Health check
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ Servidor está rodando")
                logger.info(f"📊 Versão: {data.get('version', 'N/A')}")
                
                # Verificar serviços
                services = data.get('services', {})
                tts_service = services.get('tts_service', {})
                
                if tts_service.get('status') == 'healthy':
                    logger.info("✅ Serviço TTS está saudável")
                    
                    engines = tts_service.get('engines', {})
                    for engine_name, engine_info in engines.items():
                        status = engine_info.get('status', 'unknown')
                        available = engine_info.get('available', False)
                        logger.info(f"🎭 {engine_name}: Status={status}, Disponível={available}")
                        
                        if engine_name == 'xtts_v2' and not available:
                            logger.error("❌ XTTS v2 não está disponível!")
                        elif engine_name == 'xtts_v2' and available:
                            logger.info("✅ XTTS v2 está disponível")
                else:
                    logger.error("❌ Serviço TTS não está saudável")
                    
                return True
            else:
                logger.error(f"❌ Servidor retornou status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao verificar servidor: {e}")
            return False
    
    def test_simple_synthesis(self):
        """Testa síntese simples para isolar o problema"""
        logger.info("🔄 TESTE: Síntese simples (não clonagem)")
        
        try:
            payload = {
                "text": "Teste de síntese simples para debug.",
                "language": "pt"
            }
            
            logger.info(f"📤 Enviando: {payload}")
            
            response = requests.post(
                f"{self.base_url}/api/tts/synthesize",
                json=payload,
                timeout=60
            )
            
            logger.info(f"📥 Status resposta: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                error = data.get("error", "")
                engine = data.get("engine", "unknown")
                audio_size = len(data.get("audio_base64", ""))
                
                logger.info(f"📊 Success: {success}")
                logger.info(f"📊 Engine: {engine}")
                logger.info(f"📊 Audio size: {audio_size} chars")
                
                if error:
                    logger.error(f"❌ Erro: {error}")
                
                if success and audio_size > 0:
                    logger.info("✅ Síntese simples funcionou!")
                    return True
                else:
                    logger.error("❌ Síntese simples falhou")
                    return False
            else:
                logger.error(f"❌ Resposta HTTP: {response.status_code}")
                logger.error(f"Conteúdo: {response.text[:500]}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro na síntese simples: {e}")
            return False
    
    def test_voice_cloning_detailed(self):
        """Testa clonagem de voz com debug detalhado"""
        logger.info("🔄 TESTE: Clonagem de voz (debug detalhado)")
        
        try:
            payload = {
                "text": "Este é um teste detalhado de clonagem de voz para identificar onde está falhando exatamente.",
                "language": "pt"
            }
            
            logger.info(f"📤 Enviando para clonagem: {payload}")
            
            # Fazer requisição com timeout longo
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/tts/clone-voice",
                json=payload,
                timeout=180  # 3 minutos
            )
            end_time = time.time()
            
            duration = end_time - start_time
            logger.info(f"📥 Status resposta: {response.status_code}")
            logger.info(f"⏱️ Tempo de resposta: {duration:.2f}s")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get("success", False)
                    error = data.get("error", "")
                    engine = data.get("engine", "unknown")
                    message = data.get("message", "")
                    audio_size = len(data.get("audio_base64", ""))
                    
                    logger.info(f"📊 Success: {success}")
                    logger.info(f"📊 Engine: {engine}")
                    logger.info(f"📊 Message: {message}")
                    logger.info(f"📊 Audio size: {audio_size} chars")
                    
                    if error:
                        logger.error(f"❌ Erro detalhado: {error}")
                        
                        # Analisar tipo de erro
                        error_lower = error.lower()
                        if "reference" in error_lower:
                            logger.error("🔍 PROBLEMA: Arquivo de referência")
                        elif "mecab" in error_lower:
                            logger.error("🔍 PROBLEMA: MeCab")
                        elif "memory" in error_lower:
                            logger.error("🔍 PROBLEMA: Memória")
                        elif "cuda" in error_lower or "gpu" in error_lower:
                            logger.error("🔍 PROBLEMA: GPU/CUDA")
                        elif "base64" in error_lower:
                            logger.error("🔍 PROBLEMA: Conversão base64")
                        elif "invalid file" in error_lower:
                            logger.error("🔍 PROBLEMA: Arquivo inválido")
                        else:
                            logger.error("🔍 PROBLEMA: Desconhecido")
                    
                    if success and audio_size > 0:
                        logger.info("✅ Clonagem funcionou!")
                        
                        # Testar se áudio é válido
                        try:
                            import base64
                            audio_data = base64.b64decode(data.get("audio_base64", ""))
                            if len(audio_data) > 1000:  # Pelo menos 1KB
                                logger.info(f"✅ Áudio válido: {len(audio_data)} bytes")
                                return True
                            else:
                                logger.error(f"❌ Áudio muito pequeno: {len(audio_data)} bytes")
                                return False
                        except Exception as decode_error:
                            logger.error(f"❌ Erro ao decodificar áudio: {decode_error}")
                            return False
                    else:
                        logger.error("❌ Clonagem falhou - sem áudio gerado")
                        return False
                        
                except json.JSONDecodeError as json_error:
                    logger.error(f"❌ Erro JSON: {json_error}")
                    logger.error(f"Resposta raw: {response.text[:1000]}")
                    return False
                    
            else:
                logger.error(f"❌ Resposta HTTP: {response.status_code}")
                logger.error(f"Conteúdo: {response.text[:500]}")
                
                if response.status_code == 404:
                    logger.error("🔍 PROBLEMA: Endpoint não encontrado")
                elif response.status_code == 500:
                    logger.error("🔍 PROBLEMA: Erro interno do servidor")
                elif response.status_code == 422:
                    logger.error("🔍 PROBLEMA: Dados inválidos")
                
                return False
                
        except requests.exceptions.Timeout:
            logger.error("❌ TIMEOUT: Clonagem demorou mais de 3 minutos")
            logger.error("🔍 PROBLEMA: Processo muito lento ou travado")
            return False
        except Exception as e:
            logger.error(f"❌ Erro na clonagem: {e}")
            logger.error(f"🔍 Tipo do erro: {type(e).__name__}")
            return False
    
    def run_comprehensive_test(self):
        """Executa teste abrangente"""
        logger.info("🧪 INICIANDO TESTE ABRANGENTE DO SERVIDOR")
        logger.info("=" * 70)
        
        tests_passed = 0
        total_tests = 3
        
        # Teste 1: Status do servidor
        if self.check_server_status():
            tests_passed += 1
            logger.info("✅ TESTE 1 PASSOU: Status do servidor")
        else:
            logger.error("❌ TESTE 1 FALHOU: Status do servidor")
            return
        
        # Teste 2: Síntese simples
        if self.test_simple_synthesis():
            tests_passed += 1
            logger.info("✅ TESTE 2 PASSOU: Síntese simples")
        else:
            logger.error("❌ TESTE 2 FALHOU: Síntese simples")
        
        # Teste 3: Clonagem de voz
        if self.test_voice_cloning_detailed():
            tests_passed += 1
            logger.info("✅ TESTE 3 PASSOU: Clonagem de voz")
        else:
            logger.error("❌ TESTE 3 FALHOU: Clonagem de voz")
        
        # Resultado final
        logger.info("=" * 70)
        logger.info("📊 RESULTADO FINAL DO DEBUG")
        logger.info("=" * 70)
        
        if tests_passed == total_tests:
            logger.info("🎉 TODOS OS TESTES PASSARAM!")
            logger.info("✅ Sistema está funcionando corretamente")
            print("\n🎯 DIAGNÓSTICO: Sistema OK")
            
        elif tests_passed == 2:
            logger.warning("⚠️ SÍNTESE FUNCIONA, CLONAGEM FALHA")
            logger.info("✅ Servidor e síntese simples funcionam")
            logger.error("❌ Problema específico na clonagem de voz")
            
            print("\n🔍 DIAGNÓSTICO:")
            print("✅ Servidor está funcionando")
            print("✅ Síntese simples funciona")
            print("❌ PROBLEMA: Clonagem de voz")
            print("💡 Verifique XTTS v2 ou arquivos de referência")
            
        elif tests_passed == 1:
            logger.warning("⚠️ APENAS STATUS FUNCIONA")
            logger.info("✅ Servidor responde")
            logger.error("❌ TTS não funciona (nem síntese nem clonagem)")
            
            print("\n🔍 DIAGNÓSTICO:")
            print("✅ Servidor conecta")
            print("❌ PROBLEMA: TTS não funciona")
            print("💡 Verifique engines TTS")
            print("💡 Verifique dependências")
            
        else:
            logger.error("❌ TODOS OS TESTES FALHARAM")
            logger.error("❌ Servidor não está funcionando")
            
            print("\n🔍 DIAGNÓSTICO:")
            print("❌ PROBLEMA: Servidor não funciona")
            print("💡 Verifique se servidor está rodando")
            print("💡 Execute: start_enhanced_correct.bat")

def main():
    """Função principal"""
    print("🔍 DEBUG DOS LOGS DO SERVIDOR EM TEMPO REAL")
    print("Este script monitora exatamente onde está falhando a geração de áudio")
    print("=" * 80)
    
    monitor = ServerLogMonitor()
    monitor.run_comprehensive_test()
    
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Se síntese simples falha → Problema nos engines TTS")
    print("2. Se clonagem falha → Problema no XTTS v2 ou referência")
    print("3. Se tudo falha → Problema no servidor")
    
    print("\n🔧 PARA CORRIGIR:")
    print("- Reinicie o servidor: start_enhanced_correct.bat")
    print("- Teste com arquivo real: python test_with_real_voice_file.py")
    print("- Verifique logs do servidor no terminal")

if __name__ == "__main__":
    main()