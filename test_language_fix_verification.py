#!/usr/bin/env python3
"""
Teste para verificar se a correção do idioma pt-BR -> pt funcionou
"""

import requests
import json
import time

def test_voice_cloning_with_pt():
    """Testa a clonagem de voz com o código de idioma 'pt' corrigido"""
    
    print("🧪 Testando clonagem de voz com idioma 'pt'...")
    
    # Dados para teste
    test_data = {
        "text": "Olá, esta é a sua voz clonada falando em português.",
        "voice_name": "crianca",
        "language": "pt"  # Usando 'pt' em vez de 'pt-BR'
    }
    
    try:
        print(f"📤 Enviando requisição para clonagem...")
        print(f"   Texto: {test_data['text']}")
        print(f"   Voz: {test_data['voice_name']}")
        print(f"   Idioma: {test_data['language']}")
        
        response = requests.post(
            "http://localhost:8000/clone-voice",
            json=test_data,
            timeout=30
        )
        
        print(f"📥 Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Clonagem bem-sucedida!")
            print(f"   Áudio gerado: {len(result.get('audio', ''))} caracteres base64")
            print(f"   Método usado: {result.get('method', 'não especificado')}")
            return True
        else:
            print(f"❌ Erro na clonagem: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando teste de verificação da correção de idioma...")
    success = test_voice_cloning_with_pt()
    
    if success:
        print("\n🎉 Correção do idioma funcionou perfeitamente!")
    else:
        print("\n⚠️ Ainda há problemas com a clonagem de voz")