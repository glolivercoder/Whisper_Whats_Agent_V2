#!/usr/bin/env python3
"""
Teste simples do endpoint de vozes
"""

import requests
import json

def test_voices():
    try:
        print("🎭 Testando endpoint de vozes clonadas...")
        
        # Testar se o servidor está rodando
        try:
            health_response = requests.get("http://localhost:8000/", timeout=5)
            print(f"✅ Servidor respondendo: {health_response.status_code}")
        except:
            print("❌ Servidor não está rodando")
            return False
        
        # Testar endpoint de vozes
        response = requests.get("http://localhost:8000/api/tts/list-cloned-voices", timeout=10)
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dados recebidos:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_voices()