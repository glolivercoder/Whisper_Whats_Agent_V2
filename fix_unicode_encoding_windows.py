#!/usr/bin/env python3
"""
Corrige problemas de encoding Unicode no Windows
"""

import re

def fix_unicode_issues():
    """Remove emojis que causam problemas no Windows"""
    
    print("🔧 Corrigindo problemas de encoding Unicode...")
    
    # Ler o arquivo
    with open('backend/main_enhanced.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituições de emojis problemáticos
    replacements = [
        ('🧹', '[CLEANUP]'),
        ('🔄', '[RELOAD]'),
        ('⚡', '[FAST]'),
        ('🚀', '[START]'),
        ('✅', '[OK]'),
        ('❌', '[ERROR]'),
        ('⚠️', '[WARNING]'),
        ('📝', '[INFO]'),
        ('🎯', '[TARGET]'),
        ('🔧', '[FIX]'),
        ('🧪', '[TEST]'),
        ('📤', '[SEND]'),
        ('📥', '[RECEIVE]'),
        ('🎉', '[SUCCESS]'),
        ('💾', '[SAVE]'),
        ('🔍', '[SEARCH]'),
        ('📊', '[STATS]'),
        ('🎵', '[AUDIO]'),
        ('🎤', '[MIC]'),
        ('🔊', '[SPEAKER]'),
    ]
    
    original_content = content
    
    for emoji, replacement in replacements:
        content = content.replace(emoji, replacement)
    
    # Verificar se houve mudanças
    if content != original_content:
        # Salvar o arquivo corrigido
        with open('backend/main_enhanced.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Emojis problemáticos removidos!")
        return True
    else:
        print("ℹ️ Nenhum emoji problemático encontrado")
        return False

if __name__ == "__main__":
    fix_unicode_issues()