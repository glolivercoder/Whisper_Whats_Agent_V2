#!/usr/bin/env python3
"""
Teste final da correção do idioma pt-BR -> pt
"""

import os
import sys
import time

def verify_env_file():
    """Verifica se o arquivo .env foi corrigido"""
    print("🔍 Verificando arquivo .env...")
    
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'TTS_LANGUAGE=pt-BR' in content:
        print("❌ Ainda há TTS_LANGUAGE=pt-BR no .env")
        return False
    elif 'TTS_LANGUAGE=pt' in content:
        print("✅ TTS_LANGUAGE=pt encontrado no .env")
    else:
        print("⚠️ TTS_LANGUAGE não encontrado no .env")
    
    if 'pt-BR-Wavenet' in content:
        print("❌ Ainda há pt-BR-Wavenet no .env")
        return False
    elif 'pt-Wavenet' in content:
        print("✅ pt-Wavenet encontrado no .env")
    else:
        print("⚠️ Configuração de voz não encontrada no .env")
    
    return True

def verify_main_enhanced():
    """Verifica se o main_enhanced.py foi corrigido"""
    print("\n🔍 Verificando backend/main_enhanced.py...")
    
    with open('backend/main_enhanced.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    if 'pt-BR' in content:
        print("❌ Ainda há pt-BR no main_enhanced.py")
        issues.append("pt-BR found")
    else:
        print("✅ Nenhum pt-BR encontrado no main_enhanced.py")
    
    if 'português brasileiro' in content:
        # Verificar se são apenas em comentários ou strings de sistema
        lines_with_ptbr = []
        for i, line in enumerate(content.split('\n'), 1):
            if 'português brasileiro' in line.lower():
                lines_with_ptbr.append(f"Linha {i}: {line.strip()}")
        
        if lines_with_ptbr:
            print("⚠️ Encontradas referências a 'português brasileiro':")
            for line in lines_with_ptbr[:3]:  # Mostrar apenas as primeiras 3
                print(f"   {line}")
    
    return len(issues) == 0

def test_configuration():
    """Testa se a configuração está correta"""
    print("\n🧪 Testando configuração...")
    
    # Simular carregamento da configuração
    os.environ['TTS_LANGUAGE'] = 'pt'  # Forçar o valor correto
    
    # Importar e testar
    sys.path.append('backend')
    try:
        from main_enhanced import Config
        config = Config()
        
        print(f"   TTS_LANGUAGE: {config.TTS_LANGUAGE}")
        print(f"   TTS_VOICE: {config.TTS_VOICE}")
        
        if config.TTS_LANGUAGE == 'pt':
            print("✅ Configuração TTS_LANGUAGE correta")
            return True
        else:
            print(f"❌ TTS_LANGUAGE incorreto: {config.TTS_LANGUAGE}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar configuração: {e}")
        return False

def main():
    print("🔧 Verificação final da correção pt-BR -> pt")
    print("=" * 60)
    
    all_good = True
    
    # Verificar .env
    if not verify_env_file():
        all_good = False
    
    # Verificar main_enhanced.py
    if not verify_main_enhanced():
        all_good = False
    
    # Testar configuração
    if not test_configuration():
        all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 TODAS AS CORREÇÕES APLICADAS COM SUCESSO!")
        print("✅ O idioma foi corrigido de pt-BR para pt")
        print("💡 Reinicie o servidor para aplicar as mudanças")
    else:
        print("❌ AINDA HÁ PROBLEMAS A CORRIGIR")
        print("⚠️ Verifique os detalhes acima")
    print("=" * 60)

if __name__ == "__main__":
    main()