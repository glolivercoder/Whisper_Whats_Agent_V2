#!/usr/bin/env python3
"""
Corrige códigos de idioma pt-br/pt-BR para pt
"""

def fix_language_codes():
    """Corrige códigos de idioma no backend"""
    print("🔧 CORRIGINDO CÓDIGOS DE IDIOMA PT-BR PARA PT")
    print("=" * 50)
    
    main_file = "backend/main_enhanced.py"
    
    # Ler arquivo
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contar ocorrências antes
    count_br = content.count('pt-br') + content.count('pt-BR')
    print(f"📋 Encontradas {count_br} ocorrências de pt-br/pt-BR")
    
    # Substituir todas as ocorrências
    content = content.replace('"pt-br"', '"pt"')
    content = content.replace('"pt-BR"', '"pt"')
    content = content.replace("'pt-br'", "'pt'")
    content = content.replace("'pt-BR'", "'pt'")
    
    # Salvar arquivo
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Contar ocorrências depois
    with open(main_file, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    count_after = new_content.count('pt-br') + new_content.count('pt-BR')
    
    print(f"✅ Correção concluída")
    print(f"📊 Ocorrências restantes: {count_after}")
    
    if count_after == 0:
        print("🎉 Todos os códigos de idioma foram corrigidos!")
        return True
    else:
        print("⚠️ Ainda há ocorrências restantes")
        return False

if __name__ == "__main__":
    success = fix_language_codes()
    
    if success:
        print("\n🎉 CORREÇÃO DE IDIOMA CONCLUÍDA!")
        print("Agora o XTTS v2 deve aceitar o idioma português")
    else:
        print("\n⚠️ Verifique manualmente as ocorrências restantes")