#!/usr/bin/env python3
"""
Script simples para iniciar o WhatsApp Voice Agent V2
"""

import subprocess
import sys
import os
import socket
import time

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Conecta a um servidor externo para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def install_requirements():
    """Instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    try:
        import fastapi
        import uvicorn
        import whisper
        print("✅ Dependências já instaladas")
        return True
    except ImportError:
        print("📚 Instalando dependências...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar dependências")
            print("💡 Execute manualmente: pip install -r requirements.txt")
            return False

def start_server():
    """Inicia o servidor FastAPI"""
    print("🚀 Iniciando servidor FastAPI...")
    
    # Criar diretórios necessários
    os.makedirs("static", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Obter IP local
    local_ip = get_local_ip()
    
    print(f"""
    
🎉 WhatsApp Voice Agent V2 está iniciando...

📱 Interfaces disponíveis:
   • Local: http://localhost:8000
   • Rede: http://{local_ip}:8000
   
🔗 WhatsApp Webhook:
   • Configure: http://{local_ip}:8000/api/whatsapp/webhook
   
💡 Dicas:
   • Use o celular na mesma WiFi para testar
   • Permita acesso ao microfone no navegador
   • Aguarde o download do modelo Whisper (primeira execução)
   
⏰ Carregando modelo Whisper... (pode demorar na primeira vez)
""")
    
    # Mudar para diretório backend
    os.chdir("backend")
    
    # Iniciar servidor
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

def main():
    """Função principal"""
    print("🤖 WhatsApp Voice Agent V2 - Quick Start")
    print("=" * 50)
    
    # Verificar se está no diretório correto
    if not os.path.exists("backend/main.py"):
        print("❌ Execute este script no diretório raiz do projeto")
        print("💡 Deve conter: backend/main.py, templates/index.html")
        sys.exit(1)
    
    # Instalar dependências
    if not install_requirements():
        sys.exit(1)
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()