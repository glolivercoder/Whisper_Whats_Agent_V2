#!/usr/bin/env python3
"""
Testa se a correção da voz clonada funcionou
"""

import sys
import os
sys.path.append('backend')

def test_cloned_voice_fix():
    """Testa se a voz clonada está usando o método correto"""
    print("🧪 TESTANDO CORREÇÃO DA VOZ CLONADA")
    print("=" * 50)
    
    try:
        # Configurar licença
        os.environ["COQUI_TOS_AGREED"] = "1"
        
        # Importar classe do backend
        from main_enhanced import TTSService
        
        # Criar instância do serviço TTS
        print("🔄 Inicializando TTSService...")
        tts_service = TTSService()
        
        if not tts_service.coqui_tts:
            print("❌ Coqui TTS não carregado")
            return False
        
        print("✅ TTSService inicializado")
        
        # Testar método clone_voice_working diretamente
        print("\n🔄 Testando método clone_voice_working...")
        
        result = tts_service.clone_voice_working(
            text="Teste de clonagem de voz funcionando.",
            language="pt"
        )
        
        if result["success"]:
            print("✅ Método clone_voice_working funcionou!")
            print(f"📊 Tamanho do áudio: {len(result.get('audio_base64', ''))} chars base64")
        else:
            print(f"❌ Método clone_voice_working falhou: {result.get('error')}")
            return False
        
        # Testar synthesize_speech com voz clonada
        print("\n🔄 Testando synthesize_speech com voz clonada...")
        
        import asyncio
        
        async def test_synthesize():
            result = await tts_service.synthesize_speech(
                text="Teste de voz clonada via synthesize_speech.",
                voice="cloned_test",
                engine="coqui"
            )
            return result
        
        result = asyncio.run(test_synthesize())
        
        if result["success"]:
            print("✅ synthesize_speech com voz clonada funcionou!")
            print(f"📊 Tamanho do áudio: {len(result.get('audio_base64', ''))} chars base64")
            return True
        else:
            print(f"❌ synthesize_speech com voz clonada falhou: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    success = test_cloned_voice_fix()
    
    if success:
        print("\n🎉 CORREÇÃO DA VOZ CLONADA FUNCIONOU!")
        print("O servidor agora deve usar o método que funciona")
    else:
        print("\n❌ Ainda há problemas com a voz clonada")
    
    return success

if __name__ == "__main__":
    success = main()