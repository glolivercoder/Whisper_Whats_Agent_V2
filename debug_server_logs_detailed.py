#!/usr/bin/env python3
"""
Debug detalhado dos logs do servidor para identificar problemas na clonagem
"""

import subprocess
import time
import requests
import json
import threading
from datetime import datetime

def monitor_server_logs():
    """Monitora os logs do servidor em tempo real"""
    print("📊 Monitorando logs do servidor...")
    
    try:
        # Iniciar o servidor e capturar logs
        process = subprocess.Popen(
            ['python', '-m', 'uvicorn', 'main_enhanced:app', '--host', '0.0.0.0', '--port', '8000'],
            cwd='backend',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Aguardar inicialização
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(10)
        
        # Thread para monitorar logs
        def log_monitor():
            while True:
                line = process.stdout.readline()
                if line:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] {line.strip()}")
                if process.poll() is not None:
                    break
        
        log_thread = threading.Thread(target=log_monitor, daemon=True)
        log_thread.start()
        
        # Aguardar um pouco mais
        time.sleep(5)
        
        # Testar clonagem de voz
        print("\n🧪 Testando clonagem de voz...")
        test_data = {
            "text": "Teste de clonagem com idioma português corrigido.",
            "voice_name": "crianca",
            "language": "pt"
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/clone-voice",
                json=test_data,
                timeout=60
            )
            
            print(f"\n📥 Resposta da clonagem:")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Sucesso: {result.get('success', False)}")
                print(f"   Método: {result.get('method', 'não especificado')}")
                print(f"   Áudio: {len(result.get('audio', ''))} chars")
            else:
                print(f"   Erro: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
        
        # Aguardar mais logs
        print("\n⏳ Aguardando mais logs por 30 segundos...")
        time.sleep(30)
        
        return process
        
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return None

if __name__ == "__main__":
    print("🔍 Iniciando debug detalhado dos logs...")
    
    server_process = monitor_server_logs()
    
    if server_process:
        print("\n🛑 Parando servidor...")
        server_process.terminate()
        time.sleep(2)
        if server_process.poll() is None:
            server_process.kill()
        print("✅ Debug concluído.")