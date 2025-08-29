#!/usr/bin/env python3
"""
Teste do sistema TTS limpo integrado
"""

import requests
import json
import subprocess
import time
import threading
from datetime import datetime

def test_clean_tts():
    """Testa o sistema TTS limpo"""
    
    print("🧪 TESTE DO SISTEMA TTS LIMPO")
    print("=" * 50)
    
    # Iniciar servidor
    print("🚀 Iniciando servidor...")
    process = subprocess.Popen(
        ['python', '-m', 'uvicorn', 'main_enhanced:app', '--host', '0.0.0.0', '--port', '8000'],
        cwd='backend',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    server_ready = False
    
    def monitor_logs():
        nonlocal server_ready
        while True:
            line = process.stdout.readline()
            if line:
                print(f"[LOG] {line.strip()}")
                if "Application startup complete" in line:
                    server_ready = True
            if process.poll() is not None:
                break
    
    log_thread = threading.Thread(target=monitor_logs, daemon=True)
    log_thread.start()
    
    # Aguardar servidor
    print("⏳ Aguardando servidor...")
    timeout = 60
    start_time = time.time()
    
    while not server_ready and (time.time() - start_time) < timeout:
        time.sleep(1)
    
    if not server_ready:
        print("❌ Servidor não inicializou")
        process.terminate()
        return False
    
    print("✅ Servidor pronto!")
    time.sleep(3)
    
    # Testar clonagem
    print("\n🧪 Testando clonagem de voz...")
    
    test_data = {
        "text": "Olá, este é um teste do sistema TTS limpo com clonagem de voz.",
        "voice_name": "Julia",
        "language": "pt"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/tts/test-clone",
            json=test_data,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("🎉 SUCESSO! Sistema TTS limpo funcionando!")
                print(f"Método: {result.get('method')}")
                print(f"Áudio: {len(result.get('audio', ''))} chars")
                success = True
            else:
                print(f"❌ Falha: {result.get('error')}")
                success = False
        else:
            print(f"❌ Erro HTTP: {response.text}")
            success = False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        success = False
    
    # Parar servidor
    print("\n🛑 Parando servidor...")
    process.terminate()
    time.sleep(2)
    if process.poll() is None:
        process.kill()
    
    return success

if __name__ == "__main__":
    success = test_clean_tts()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SISTEMA TTS LIMPO FUNCIONANDO!")
    else:
        print("❌ Sistema ainda tem problemas")
    print("=" * 50)
