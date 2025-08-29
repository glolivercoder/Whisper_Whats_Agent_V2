#!/usr/bin/env python3
"""
Teste do endpoint de listar vozes clonadas
"""

import requests
import json
import subprocess
import sys
import time
from threading import Thread

def start_server():
    """Inicia servidor"""
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.main_enhanced:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ]
    
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

def wait_for_server(timeout=30):
    """Aguarda servidor"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code in [200, 404]:
                return True
        except:
            pass
        time.sleep(1)
    return False

def test_list_cloned_voices():
    """Testa endpoint de listar vozes"""
    print("🎭 TESTANDO ENDPOINT DE VOZES CLONADAS")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8000/api/tts/list-cloned-voices", timeout=10)
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta recebida:")
            print(f"   Success: {data.get('success')}")
            print(f"   Total de vozes: {data.get('total', 0)}")
            print(f"   Vozes clonadas: {data.get('cloned_voices', 0)}")
            print(f"   Vozes de referência: {data.get('reference_voices', 0)}")
            
            voices = data.get('voices', [])
            if voices:
                print(f"\n📋 VOZES DISPONÍVEIS:")
                for i, voice in enumerate(voices, 1):
                    voice_type = voice.get('type', 'cloned')
                    icon = "🎤" if voice_type == "reference" else "🎭"
                    print(f"   {i}. {icon} {voice.get('name')} ({voice.get('language', 'pt')})")
                    if voice.get('display_name'):
                        print(f"      Nome: {voice.get('display_name')}")
                    if voice.get('date_created'):
                        print(f"      Criado: {voice.get('date_created')}")
            else:
                print("   Nenhuma voz encontrada")
            
            return True
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def main():
    print("🧪 TESTE DO ENDPOINT DE VOZES CLONADAS")
    print("=" * 60)
    
    # Iniciar servidor
    server_process = start_server()
    
    try:
        print("🚀 Iniciando servidor...")
        
        if not wait_for_server():
            print("❌ Servidor não iniciou")
            return False
        
        print("✅ Servidor pronto!")
        
        # Testar endpoint
        success = test_list_cloned_voices()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 TESTE DO ENDPOINT: SUCESSO!")
        else:
            print("❌ TESTE DO ENDPOINT: FALHOU!")
        print("=" * 60)
        
        return success
        
    finally:
        print("\n🛑 Parando servidor...")
        try:
            server_process.terminate()
            server_process.wait(timeout=10)
        except:
            server_process.kill()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)