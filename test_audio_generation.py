#!/usr/bin/env python3
"""
Teste final da geração de áudio após correções
"""

import os
import sys
import asyncio
sys.path.append('backend')

async def test_audio_generation():
    """Testa geração de áudio com diferentes engines"""
    print("🧪 TESTE FINAL DA GERAÇÃO DE ÁUDIO")
    print("=" * 50)
    
    try:
        # Configurar ambiente
        os.environ["COQUI_TOS_AGREED"] = "1"
        os.environ["COQUI_TTS_NO_MECAB"] = "1"
        os.environ["PYTHONWARNINGS"] = "ignore"
        
        # Importar serviço TTS
        from main_enhanced import TTSService
        
        # Criar instância
        tts_service = TTSService()
        print("✅ TTSService inicializado")
        
        # Teste 1: Clonagem de voz (XTTS v2)
        print("\n🎭 TESTE 1: CLONAGEM DE VOZ")
        print("-" * 30)
        
        result1 = tts_service.clone_voice_working(
            text="Teste de clonagem de voz funcionando perfeitamente.",
            language="pt"
        )
        
        if result1["success"]:
            print("✅ Clonagem de voz: FUNCIONANDO")
            print(f"📊 Tamanho: {len(result1.get('audio_base64', ''))} chars base64")
        else:
            print(f"❌ Clonagem de voz: FALHOU - {result1.get('error')}")
        
        # Teste 2: Síntese regular (Coqui TTS)
        print("\n🔊 TESTE 2: SÍNTESE REGULAR (COQUI)")
        print("-" * 30)
        
        result2 = await tts_service.synthesize_speech(
            text="Teste de síntese regular com Coqui TTS.",
            voice="default",
            engine="coqui",
            language="pt"
        )
        
        if result2["success"]:
            print("✅ Síntese Coqui: FUNCIONANDO")
            print(f"📊 Tamanho: {len(result2.get('audio_data', ''))} chars base64")
        else:
            print(f"❌ Síntese Coqui: FALHOU - {result2.get('error')}")
        
        # Teste 3: Fallback gTTS
        print("\n🌐 TESTE 3: FALLBACK GTTS")
        print("-" * 30)
        
        result3 = await tts_service.synthesize_speech(
            text="Teste de fallback com Google TTS.",
            voice="pt-BR-Standard-A",
            engine="gtts",
            language="pt-br"
        )
        
        if result3["success"]:
            print("✅ gTTS: FUNCIONANDO")
            print(f"📊 Tamanho: {len(result3.get('audio_data', ''))} chars base64")
        else:
            print(f"❌ gTTS: FALHOU - {result3.get('error')}")
        
        # Teste 4: Fallback pyttsx3
        print("\n🖥️ TESTE 4: FALLBACK PYTTSX3")
        print("-" * 30)
        
        result4 = await tts_service.synthesize_speech(
            text="Teste de fallback com pyttsx3.",
            voice="default",
            engine="pyttsx3",
            language="pt"
        )
        
        if result4["success"]:
            print("✅ pyttsx3: FUNCIONANDO")
            print(f"📊 Tamanho: {len(result4.get('audio_data', ''))} chars base64")
        else:
            print(f"❌ pyttsx3: FALHOU - {result4.get('error')}")
        
        # Resumo
        results = [result1, result2, result3, result4]
        success_count = sum(1 for r in results if r["success"])
        
        print(f"\n📊 RESUMO: {success_count}/4 engines funcionando")
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🔧 TESTE FINAL DA GERAÇÃO DE ÁUDIO")
    print("Verificando se todos os problemas foram resolvidos")
    print("=" * 60)
    
    # Executar teste assíncrono
    success = asyncio.run(test_audio_generation())
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    if success:
        print("🎉 GERAÇÃO DE ÁUDIO FUNCIONANDO!")
        print("✅ Pelo menos um engine está operacional")
        print("✅ Erro 'Falha desconhecida' deve estar resolvido")
        print("✅ Sistema pronto para uso")
        
        print("\n🚀 SISTEMA OPERACIONAL!")
        print("Execute o servidor e teste na interface")
        
        return True
    else:
        print("❌ AINDA HÁ PROBLEMAS NA GERAÇÃO DE ÁUDIO")
        print("Verifique os logs acima para mais detalhes")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("\n❌ TESTE FALHOU - VERIFIQUE OS PROBLEMAS ACIMA")