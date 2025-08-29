#!/usr/bin/env python3
"""
Teste garantido de geração de áudio
"""

import requests
import subprocess
import time
import sys
import os
import base64
from threading import Thread

class AudioGenerationTester:
    def __init__(self):
        self.server_process = None
        self.server_ready = False
    
    def start_server(self):
        """Inicia o servidor corrigido"""
        print("🚀 Iniciando servidor com correções de áudio...")
        
        try:
            self.server_process = subprocess.Popen(
                ["./start_enhanced_correct.bat"],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Monitor logs
            Thread(target=self.monitor_logs, daemon=True).start()
            
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
            return False
    
    def monitor_logs(self):
        """Monitora logs do servidor"""
        if not self.server_process:
            return
            
        for line in iter(self.server_process.stdout.readline, ''):
            if line:
                print(f"[SERVER] {line.strip()}")
                if "Application startup complete" in line or "Uvicorn running" in line:
                    self.server_ready = True
    
    def wait_for_server(self, timeout=120):
        """Aguarda servidor ficar pronto"""
        print("⏳ Aguardando servidor...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:8001/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Servidor pronto!")
                    return True
            except:
                pass
            
            time.sleep(2)
        
        print("❌ Timeout aguardando servidor")
        return False
    
    def test_audio_generation_detailed(self):
        """Teste detalhado de geração de áudio"""
        print("\\n🎭 TESTE DETALHADO DE GERAÇÃO DE ÁUDIO")
        print("=" * 60)
        
        # 1. Verificar vozes disponíveis
        print("📋 Verificando vozes disponíveis...")
        try:
            response = requests.get("http://localhost:8001/api/tts/list-cloned-voices", timeout=30)
            if response.status_code == 200:
                voices_data = response.json()
                voices = voices_data.get('voices', [])
                print(f"✅ {len(voices)} vozes encontradas")
                
                if not voices:
                    print("❌ Nenhuma voz disponível!")
                    return False
                
                # Usar a primeira voz disponível
                test_voice = voices[0]['name']
                print(f"🎤 Usando voz: {test_voice}")
            else:
                print(f"❌ Erro ao listar vozes: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro ao verificar vozes: {e}")
            return False
        
        # 2. Teste de geração de áudio
        print(f"\\n🎵 Testando geração de áudio com {test_voice}...")
        
        test_data = {
            "text": "Este é um teste definitivo de geração de áudio. O sistema deve funcionar perfeitamente agora.",
            "voice": test_voice,
            "language": "pt",
            "engine": "xtts_v2"
        }
        
        try:
            print(f"📤 Enviando requisição: {test_data}")
            
            response = requests.post(
                "http://localhost:8001/api/tts",
                json=test_data,
                timeout=120
            )
            
            print(f"📥 Status HTTP: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print("📊 ANÁLISE DA RESPOSTA:")
                print(f"   Success: {result.get('success')}")
                print(f"   Message: {result.get('message')}")
                print(f"   Engine: {result.get('engine')}")
                print(f"   Voice: {result.get('voice_name')}")
                print(f"   File Size: {result.get('file_size', 0)} bytes")
                
                # Verificar áudio
                audio_data = result.get('audio_data')
                if audio_data:
                    audio_size = len(audio_data)
                    print(f"   Audio Data: {audio_size} caracteres")
                    
                    # Verificar se é base64 válido
                    try:
                        decoded = base64.b64decode(audio_data)
                        decoded_size = len(decoded)
                        print(f"   Audio Decoded: {decoded_size} bytes")
                        
                        if decoded_size > 10000:  # Pelo menos 10KB
                            print("🎉 ÁUDIO GERADO COM SUCESSO!")
                            print(f"✅ Tamanho adequado: {decoded_size} bytes")
                            
                            # Salvar arquivo para verificação
                            with open("test_audio_output.wav", "wb") as f:
                                f.write(decoded)
                            print("💾 Áudio salvo como: test_audio_output.wav")
                            
                            return True
                        else:
                            print(f"❌ Áudio muito pequeno: {decoded_size} bytes")
                            return False
                            
                    except Exception as e:
                        print(f"❌ Erro ao decodificar base64: {e}")
                        return False
                else:
                    print("❌ Nenhum áudio retornado!")
                    return False
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False
    
    def stop_server(self):
        """Para o servidor"""
        if self.server_process:
            print("🛑 Parando servidor...")
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=10)
            except:
                self.server_process.kill()
    
    def run_complete_test(self):
        """Executa teste completo"""
        print("🧪 TESTE COMPLETO DE GERAÇÃO DE ÁUDIO")
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
            
            # Testar geração de áudio
            success = self.test_audio_generation_detailed()
            
            print("\\n" + "=" * 60)
            if success:
                print("🎉 TESTE COMPLETO: SUCESSO!")
                print("✅ Geração de áudio funcionando perfeitamente!")
                print("✅ Sistema pronto para uso!")
            else:
                print("❌ TESTE COMPLETO: FALHOU!")
                print("❌ Geração de áudio não está funcionando")
            print("=" * 60)
            
            return success
            
        finally:
            self.stop_server()

def main():
    tester = AudioGenerationTester()
    return tester.run_complete_test()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)