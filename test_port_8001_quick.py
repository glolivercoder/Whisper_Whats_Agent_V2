#!/usr/bin/env python3
"""
Teste rápido para verificar se o servidor está funcionando na porta 8001
"""

import requests
import subprocess
import time
import sys
import os
from threading import Thread

def test_server_port_8001():
    """Testa se o servidor está respondendo na porta 8001"""
    print("🧪 TESTE RÁPIDO - PORTA 8001")
    print("=" * 50)
    
    # Primeiro, verificar se o servidor já está rodando
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor já está rodando na porta 8001!")
            return test_endpoints()
        else:
            print(f"⚠️ Servidor respondeu com status {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Servidor não está rodando na porta 8001")
        print("💡 Execute: start_enhanced_correct.bat")
        return False

def test_endpoints():
    """Testa os endpoints principais"""
    print("\n🔍 TESTANDO ENDPOINTS...")
    
    endpoints = [
        ("Health Check", "http://localhost:8001/health"),
        ("API Status", "http://localhost:8001/api/status"),
        ("TTS Status", "http://localhost:8001/api/tts/status"),
        ("List Voices", "http://localhost:8001/api/tts/list-cloned-voices")
    ]
    
    all_ok = True
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: Status {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ {name}: Erro - {e}")
            all_ok = False
    
    return all_ok

def test_voice_cloning():
    """Teste rápido de clonagem de voz"""
    print("\n🎭 TESTANDO CLONAGEM DE VOZ...")
    
    data = {
        "text": "Teste rápido de clonagem de voz.",
        "voice": "Julia",
        "language": "pt",
        "engine": "xtts_v2"
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/api/tts",
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('audio_data'):
                print("✅ Clonagem de voz funcionando!")
                return True
            else:
                print(f"❌ Clonagem falhou: {result.get('message', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na clonagem: {e}")
        return False

def main():
    print("🚀 VERIFICAÇÃO RÁPIDA DO SISTEMA")
    print("=" * 50)
    
    # Testar se servidor está rodando
    if not test_server_port_8001():
        print("\n❌ FALHA: Servidor não está funcionando")
        print("💡 Execute: start_enhanced_correct.bat")
        return False
    
    # Testar clonagem de voz
    if test_voice_cloning():
        print("\n🎉 SUCESSO TOTAL!")
        print("✅ Servidor funcionando na porta 8001")
        print("✅ Clonagem de voz funcionando")
        print("✅ Interface pode acessar http://localhost:8001")
        return True
    else:
        print("\n⚠️ PARCIAL: Servidor OK, mas clonagem com problemas")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)