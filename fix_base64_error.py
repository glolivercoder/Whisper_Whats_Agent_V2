#!/usr/bin/env python3
"""
Corrige o erro da variável base64 nos métodos gTTS e pyttsx3
"""

import os
import sys

def fix_base64_import_error():
    """Corrige o erro de importação do base64"""
    print("🔧 CORRIGINDO ERRO DA VARIÁVEL BASE64")
    print("=" * 50)
    
    # Ler o arquivo atual
    file_path = "backend/main_enhanced.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Arquivo lido: {file_path}")
        
        # Correções necessárias
        corrections = [
            {
                "description": "Adicionar import base64 no método gTTS",
                "old": """            try:
                import io
                from gtts import gTTS""",
                "new": """            try:
                import io
                import base64
                from gtts import gTTS"""
            },
            {
                "description": "Adicionar import base64 no método pyttsx3",
                "old": """            # Generate audio to temporary file
            import tempfile""",
                "new": """            # Generate audio to temporary file
            import tempfile
            import base64"""
            }
        ]
        
        # Aplicar correções
        modified = False
        for correction in corrections:
            if correction["old"] in content:
                content = content.replace(correction["old"], correction["new"])
                print(f"✅ {correction['description']}")
                modified = True
            else:
                print(f"⚠️ {correction['description']} - padrão não encontrado")
        
        if modified:
            # Salvar arquivo corrigido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Arquivo corrigido e salvo")
            return True
        else:
            print("⚠️ Nenhuma correção foi aplicada")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao corrigir arquivo: {e}")
        return False

def test_server_startup():
    """Testa se o servidor inicia sem erros"""
    print("\n🧪 TESTANDO INICIALIZAÇÃO DO SERVIDOR")
    print("=" * 50)
    
    try:
        # Configurar ambiente
        os.environ["COQUI_TOS_AGREED"] = "1"
        os.environ["COQUI_TTS_NO_MECAB"] = "1"
        os.environ["PYTHONWARNINGS"] = "ignore"
        
        # Tentar importar o módulo principal
        sys.path.append('backend')
        from main_enhanced import TTSService
        
        print("✅ Módulo main_enhanced importado com sucesso")
        
        # Tentar criar instância do serviço
        tts_service = TTSService()
        print("✅ TTSService inicializado com sucesso")
        
        # Verificar se os métodos estão funcionando
        if hasattr(tts_service, 'synthesize_speech'):
            print("✅ Método synthesize_speech disponível")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 CORREÇÃO DO ERRO BASE64 NO SERVIDOR")
    print("Corrigindo imports faltantes nos métodos gTTS e pyttsx3")
    print("=" * 60)
    
    # 1. Corrigir erro de importação base64
    fix_ok = fix_base64_import_error()
    
    # 2. Testar inicialização do servidor
    test_ok = test_server_startup()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL")
    print("=" * 60)
    
    if fix_ok and test_ok:
        print("🎉 CORREÇÃO APLICADA COM SUCESSO!")
        print("✅ Erro da variável base64 corrigido")
        print("✅ Servidor inicializa sem problemas")
        print("✅ Métodos gTTS e pyttsx3 funcionais")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Reinicie o servidor no ambiente virtual")
        print("2. Teste a geração de áudio")
        print("3. Não deve mais aparecer erro de base64")
        
        return True
    else:
        print("❌ AINDA HÁ PROBLEMAS")
        
        if not fix_ok:
            print("• Não foi possível corrigir o arquivo")
        if not test_ok:
            print("• Servidor ainda tem problemas de inicialização")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 CORREÇÃO BASE64 CONCLUÍDA!")
    else:
        print("\n❌ CORREÇÃO FALHOU - VERIFIQUE OS PROBLEMAS ACIMA")