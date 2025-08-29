#!/usr/bin/env python3
"""
TESTE REAL DE PRODUÇÃO - SEM ENROLAÇÃO
Testa o sistema completo como se fosse um usuário real
"""

import requests
import time
import subprocess
import sys
import os
import json
from threading import Thread

def start_server():
    """Inicia o servidor real"""
    print("🚀 Iniciando servidor de produção...")
    
    # Usar o script de inicialização real
    if os.path.exists("start_enhanced_correct.bat"):
        process = subprocess.Popen(
            ["start_enhanced_correct.bat"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    else:
        # Fallback para comando direto
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.main_enhanced:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    return process

def wait_for_server(max_attempts=30):
    """Aguarda servidor ficar disponível"""
    print("⏳ Aguardando servidor...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor disponível!")
                return True
        except:
            pass
        
        time.sleep(2)
        print(f"   Tentativa {attempt + 1}/{max_attempts}...")
    
    return False

def test_voice_cloning():
    """Testa clonagem de voz REAL"""
    print("\n🎭 TESTANDO CLONAGEM DE VOZ REAL...")
    
    # Dados do teste
    test_data = {
        "text": "Este é um teste real de clonagem de voz no ambiente de produção.",
        "voice": "Julia",  # Voz que sabemos que existe
        "language": "pt",
        "engine": "xtts_v2"
    }
    
    try:
        print(f"📤 Enviando requisição: {test_data}")
        
        response = requests.post(
            "http://localhost:8000/api/tts/synthesize",
            json=test_data,
            timeout=60  # 1 minuto timeout
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Resposta recebida:")
            print(f"   - Success: {result.get('success')}")
            print(f"   - Message: {result.get('message')}")
            print(f"   - Engine: {result.get('engine', 'N/A')}")
            print(f"   - Voice: {result.get('voice_name', 'N/A')}")
            
            if result.get('audio_data'):
                audio_size = len(result['audio_data'])
                print(f"   - Áudio gerado: {audio_size} chars")
                
                if audio_size > 1000:  # Áudio válido
                    print("🎉 CLONAGEM DE VOZ FUNCIONANDO!")
                    return True
                else:
                    print("❌ Áudio muito pequeno - possível erro")
                    return False
            else:
                print("❌ Nenhum áudio retornado")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Erro: {error_data}")
            except:
                print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def test_basic_tts():
    """Testa TTS básico"""
    print("\n🔊 TESTANDO TTS BÁSICO...")
    
    test_data = {
        "text": "Teste de TTS básico sem clonagem.",
        "language": "pt"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/tts/synthesize",
            json=test_data,
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('audio_data'):
                print("✅ TTS básico funcionando!")
                return True
        
        print("❌ TTS básico falhou")
        return False
        
    except Exception as e:
        print(f"❌ Erro no TTS básico: {e}")
        return False

def main():
    """Teste principal"""
    print("=" * 60)
    print("🧪 TESTE REAL DE PRODUÇÃO - CLONAGEM DE VOZ")
    print("=" * 60)
    
    # Iniciar servidor
    server_process = start_server()
    
    try:
        # Aguardar servidor
        if not wait_for_server():
            print("❌ FALHA: Servidor não iniciou")
            return False
        
        # Testar TTS básico primeiro
        basic_ok = test_basic_tts()
        
        # Testar clonagem de voz
        clone_ok = test_voice_cloning()
        
        # Resultado final
        print("\n" + "=" * 60)
        print("📋 RESULTADO FINAL:")
        print("=" * 60)
        
        if basic_ok and clone_ok:
            print("🎉 SUCESSO TOTAL! Sistema funcionando em produção!")
            return True
        elif basic_ok:
            print("⚠️  TTS básico OK, mas clonagem falhou")
            return False
        else:
            print("❌ FALHA TOTAL! Sistema não funciona")
            return False
            
    finally:
        # Parar servidor
        print("\n🛑 Parando servidor...")
        try:
            server_process.terminate()
            server_process.wait(timeout=10)
        except:
            server_process.kill()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)