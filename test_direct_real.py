#!/usr/bin/env python3
"""
TESTE DIRETO REAL - SEM SERVIDOR
Testa diretamente o CleanTTSService
"""

import sys
import os
sys.path.append('backend')

from clean_tts_service import CleanTTSService

def test_direct():
    print("🧪 TESTE DIRETO DO CleanTTSService")
    print("=" * 50)
    
    try:
        # Criar instância
        print("📦 Criando CleanTTSService...")
        tts = CleanTTSService()
        print("✅ CleanTTSService criado")
        
        # Testar clonagem
        print("\n🎭 Testando clonagem de voz...")
        result = tts.synthesize_speech(
            text="Este é um teste direto real da clonagem de voz.",
            voice="Julia",
            language="pt"
        )
        
        print(f"📋 Resultado:")
        print(f"   Success: {result.get('success')}")
        print(f"   Message: {result.get('message')}")
        print(f"   Engine: {result.get('engine')}")
        print(f"   Voice: {result.get('voice_name')}")
        
        if result.get('audio'):
            audio_size = len(result['audio'])
            print(f"   Audio size: {audio_size} chars")
            
            if audio_size > 1000:
                print("🎉 CLONAGEM FUNCIONANDO!")
                return True
            else:
                print("❌ Áudio muito pequeno")
                return False
        else:
            print("❌ Nenhum áudio gerado")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct()
    print("\n" + "=" * 50)
    if success:
        print("🎉 TESTE DIRETO: SUCESSO!")
    else:
        print("❌ TESTE DIRETO: FALHOU!")
    print("=" * 50)