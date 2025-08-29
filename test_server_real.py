#!/usr/bin/env python3
"""
TESTE REAL DO SERVIDOR - PRODUÇÃO
"""

import requests
import time
import subprocess
import sys
import os
import signal
from threading import Thread

class ServerTester:
    def __init__(self):
        self.server_process = None
        self.server_ready = False
    
    def start_server(self):
        """Inicia servidor real"""
        print("🚀 Iniciando servidor real...")
        
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend.main_enhanced:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ]
        
        self.server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Thread para monitorar logs
        Thread(target=self.monitor_logs, daemon=True).start()
        
        return self.server_process
    
    def monitor_logs(self):
        """Monitora logs do servidor"""
        if not self.server_process:
            return
            
        for line in iter(self.server_process.stdout.readline, ''):
            if line:
                print(f"[SERVER] {line.strip()}")
                if "Application startup complete" in line:
                    self.server_ready = True
    
    def wait_for_server(self, timeout=60):
        """Aguarda servidor ficar pronto"""
        print("⏳ Aguardando servidor...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.server_ready:
                # Verificar se responde
                try:
                    response = requests.get("http://localhost:8000/", timeout=5)
                    if response.status_code in [200, 404]:  # 404 é OK, significa que está rodando
                        print("✅ Servidor pronto!")
                        return True
                except:
                    pass
            
            time.sleep(1)
        
        print("❌ Timeout aguardando servidor")
        return False
    
    def test_voice_cloning(self):
        """Testa clonagem real"""
        print("\n🎭 TESTANDO CLONAGEM DE VOZ...")
        
        data = {
            "text": "Este é um teste real de produção da clonagem de voz.",
            "voice": "Julia",
            "language": "pt",
            "engine": "xtts_v2"
        }
        
        try:
            print(f"📤 Enviando: {data}")
            
            response = requests.post(
                "http://localhost:8000/api/tts",
                json=data,
                timeout=120  # 2 minutos
            )
            
            print(f"📥 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Resposta:")
                print(f"   Success: {result.get('success')}")
                print(f"   Message: {result.get('message')}")
                print(f"   Engine: {result.get('engine')}")
                print(f"   Voice: {result.get('voice_name')}")
                
                if result.get('audio_data'):
                    size = len(result['audio_data'])
                    print(f"   Audio: {size} chars")
                    
                    if size > 1000:
                        print("🎉 CLONAGEM FUNCIONANDO NO SERVIDOR!")
                        return True
                    else:
                        print("❌ Áudio muito pequeno")
                        return False
                else:
                    print("❌ Sem áudio")
                    return False
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False
    
    def stop_server(self):
        """Para servidor"""
        if self.server_process:
            print("🛑 Parando servidor...")
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=10)
            except:
                self.server_process.kill()
    
    def run_test(self):
        """Executa teste completo"""
        print("=" * 60)
        print("🧪 TESTE REAL DO SERVIDOR DE PRODUÇÃO")
        print("=" * 60)
        
        try:
            # Iniciar servidor
            if not self.start_server():
                print("❌ Falha ao iniciar servidor")
                return False
            
            # Aguardar servidor
            if not self.wait_for_server():
                print("❌ Servidor não ficou pronto")
                return False
            
            # Testar clonagem
            success = self.test_voice_cloning()
            
            print("\n" + "=" * 60)
            if success:
                print("🎉 TESTE DE PRODUÇÃO: SUCESSO TOTAL!")
                print("✅ Sistema funcionando perfeitamente!")
            else:
                print("❌ TESTE DE PRODUÇÃO: FALHOU!")
                print("❌ Sistema não está funcionando!")
            print("=" * 60)
            
            return success
            
        finally:
            self.stop_server()

def main():
    tester = ServerTester()
    return tester.run_test()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)