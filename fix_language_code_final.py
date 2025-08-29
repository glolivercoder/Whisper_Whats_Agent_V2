#!/usr/bin/env python3
"""
Fix definitivo para o código de idioma pt-BR -> pt no XTTS v2
"""

import re

def fix_language_code():
    """Corrige o código de idioma de pt-BR para pt no main_enhanced.py"""
    
    print("🔧 Corrigindo código de idioma pt-BR -> pt...")
    
    # Ler o arquivo
    with open('backend/main_enhanced.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituições necessárias
    replacements = [
        # Nas funções de clonagem
        (r'language="pt-BR"', 'language="pt"'),
        (r"language='pt-BR'", "language='pt'"),
        (r'"pt-BR"', '"pt"'),
        (r"'pt-BR'", "'pt'"),
        
        # Em dicionários e configurações
        (r'pt-BR', 'pt'),
        
        # Comentários e logs que mencionam pt-BR
        (r'português brasileiro \(pt-BR\)', 'português (pt)'),
        (r'pt-BR \(português brasileiro\)', 'pt (português)'),
    ]
    
    original_content = content
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    # Verificar se houve mudanças
    if content != original_content:
        # Salvar o arquivo corrigido
        with open('backend/main_enhanced.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Código de idioma corrigido com sucesso!")
        print("📝 Mudanças aplicadas:")
        
        # Mostrar as linhas que foram alteradas
        old_lines = original_content.split('\n')
        new_lines = content.split('\n')
        
        for i, (old_line, new_line) in enumerate(zip(old_lines, new_lines), 1):
            if old_line != new_line:
                print(f"   Linha {i}:")
                print(f"   - {old_line.strip()}")
                print(f"   + {new_line.strip()}")
        
        return True
    else:
        print("ℹ️ Nenhuma alteração necessária encontrada")
        return False

if __name__ == "__main__":
    fix_language_code()