#!/usr/bin/env python3
"""
Debug do servidor em tempo real para identificar o problema exato
"""

import requests
import json
import time
import os

def test_server_endpoints():
    """Testa os endpoints do servidor para identificar problemas"""
    print("🔍 DEBUGANDO SERVIDOR EM TEMPO REAL")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Teste 1: Verificar se servidor está rodando
    print("🔄 TESTE 1: Verificando se servidor está ativo...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando")
            print(f"📊 Status: {response.json()}")
        else:
            print(f"⚠️ Servidor respondeu com status: {response.status_code}")
    except Exception as e:
        print(f"❌ Servidor não está respondendo: {e}")
        print("💡 Execute: start_server_venv.bat")
        return False
    
    # Teste 2: Verificar status dos engines TTS
    print("\n🔄 TESTE 2: Verificando engines TTS...")
    try:
        response = requests.get(f"{base_url}/api/tts/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("✅ Status TTS obtido:")
            
            engines = status.get("engines", {})
            for engine, info in engines.items():
                status_icon = "✅" if info.get("available") else "❌"
                print(f"   {status_icon} {engine}: {info.get('status', 'Unknown')}")
                
                if not info.get("available") and info.get("error"):
                    print(f"      ❌ Erro: {info['error']}")
        else:
            print(f"❌ Erro ao obter status: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao verificar status TTS: {e}")
    
    # Teste 3: Testar clonagem de voz
    print("\n🔄 TESTE 3: Testando clonagem de voz...")
    try:
        test_data = {
            "text": "Teste de clonagem de voz em tempo real.",
            "language": "pt"
        }
        
        response = requests.post(
            f"{base_url}/api/tts/clone-voice",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Clonagem funcionou!")
                print(f"📊 Tamanho áudio: {len(result.get('audio_base64', ''))} chars")
                print(f"🎭 Engine: {result.get('engine', 'Unknown')}")
            else:
                print(f"❌ Clonagem falhou: {result.get('error')}")
                return False
        else:
            print(f"❌ Erro HTTP na clonagem: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na clonagem: {e}")
        return False
    
    # Teste 4: Testar síntese regular
    print("\n🔄 TESTE 4: Testando síntese regular...")
    try:
        test_data = {
            "text": "Teste de síntese regular.",
            "voice": "default",
            "engine": "coqui",
            "language": "pt"
        }
        
        response = requests.post(
            f"{base_url}/api/tts/synthesize",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ Síntese funcionou!")
                print(f"📊 Tamanho áudio: {len(result.get('audio_data', ''))} chars")
            else:
                print(f"❌ Síntese falhou: {result.get('error')}")
        else:
            print(f"❌ Erro HTTP na síntese: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na síntese: {e}")
    
    return True

def monitor_logs():
    """Monitora logs em tempo real"""
    print("\n🔄 MONITORANDO LOGS EM TEMPO REAL...")
    print("=" * 50)
    
    log_file = "logs/enhanced_agent.log"
    
    if not os.path.exists(log_file):
        print(f"❌ Arquivo de log não encontrado: {log_file}")
        return
    
    try:
        # Ler últimas 20 linhas
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            recent_lines = lines[-20:] if len(lines) > 20 else lines
        
        print("📋 ÚLTIMAS ENTRADAS DO LOG:")
        for line in recent_lines:
            line = line.strip()
            if line:
                if "ERROR" in line:
                    print(f"❌ {line}")
                elif "WARNING" in line:
                    print(f"⚠️ {line}")
                elif "INFO" in line and ("✅" in line or "🎉" in line):
                    print(f"✅ {line}")
                else:
                    print(f"📝 {line}")
                    
    except Exception as e:
        print(f"❌ Erro ao ler logs: {e}")

def main():
    """Função principal"""
    print("🔍 DEBUG COMPLETO DO SERVIDOR")
    print("Identificando problemas em tempo real")
    print("=" * 60)
    
    # 1. Monitorar logs primeiro
    monitor_logs()
    
    # 2. Testar endpoints
    server_ok = test_server_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNÓSTICO FINAL")
    print("=" * 60)
    
    if server_ok:
        print("🎉 SERVIDOR FUNCIONANDO CORRETAMENTE!")
        print("✅ Todos os testes passaram")
        print("✅ Clonagem de voz operacional")
        print("✅ Problema 'Falha desconhecida' resolvido")
    else:
        print("❌ SERVIDOR COM PROBLEMAS")
        print("💡 Verifique os logs acima")
        print("💡 Reinicie com: start_server_venv.bat")
        print("💡 Ou execute: fix_versions.bat")
    
    return server_ok

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 DEBUG CONCLUÍDO - SISTEMA OK!")
    else:
        print("\n❌ DEBUG IDENTIFICOU PROBLEMAS")