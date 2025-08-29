#!/usr/bin/env python3
"""
FIX DE ERROS DE SINTAXE
=======================

Corrige todos os erros de sintaxe no main_enhanced.py
"""

import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_syntax_errors():
    """Corrige erros de sintaxe no arquivo main_enhanced.py"""
    
    main_file = "backend/main_enhanced.py"
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info("🔄 Corrigindo erros de sintaxe...")
        
        # Padrões de erro para corrigir
        fixes = [
            # Erro: return None    def method
            (r'return None\s+def ', 'return None\n\n    def '),
            
            # Erro: }    if __name__
            (r'\}\s+if __name__', '}\n\nif __name__'),
            
            # Erro: detail=...)if __name__
            (r'detail=f"[^"]*"\)\s*if __name__', lambda m: m.group(0).replace(')if', ')\n\nif')),
            
            # Erro: )    global
            (r'\)\s+global ', ')\n        global '),
            
            # Erro: statement    def method (sem quebra de linha)
            (r'([a-zA-Z0-9_\)\]\}])\s+(def [a-zA-Z_][a-zA-Z0-9_]*\()', r'\1\n\n    \2'),
            
            # Erro: statement    if __name__
            (r'([a-zA-Z0-9_\)\]\}])\s+(if __name__)', r'\1\n\n\2'),
            
            # Erro: statement    class
            (r'([a-zA-Z0-9_\)\]\}])\s+(class [A-Z][a-zA-Z0-9_]*)', r'\1\n\n\2'),
            
            # Erro: statement    import
            (r'([a-zA-Z0-9_\)\]\}])\s+(import [a-zA-Z_])', r'\1\n        \2'),
            
            # Erro: statement    from
            (r'([a-zA-Z0-9_\)\]\}])\s+(from [a-zA-Z_])', r'\1\n        \2'),
        ]
        
        # Aplicar correções
        for i, (pattern, replacement) in enumerate(fixes):
            if callable(replacement):
                content = re.sub(pattern, replacement, content)
            else:
                content = re.sub(pattern, replacement, content)
            logger.info(f"✅ Aplicada correção {i+1}")
        
        # Correções específicas adicionais
        specific_fixes = [
            # Corrigir linhas específicas conhecidas
            ('app.state.db_service = db_service    global', 'app.state.db_service = db_service\n        logger.info("✅ Services assigned to app.state")\n        \n        # Load Whisper models\n        global'),
            
            ('return None    def _prepare_mecab_environment', 'return None\n\n    def _prepare_mecab_environment'),
            
            ('detail=f"Erro interno: {str(e)}")if __name__', 'detail=f"Erro interno: {str(e)}")\n\nif __name__'),
        ]
        
        for old, new in specific_fixes:
            if old in content:
                content = content.replace(old, new)
                logger.info(f"✅ Correção específica aplicada: {old[:50]}...")
        
        # Salvar arquivo corrigido
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ Erros de sintaxe corrigidos")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao corrigir sintaxe: {e}")
        return False

def main():
    """Executa as correções"""
    logger.info("🔧 CORRIGINDO ERROS DE SINTAXE")
    logger.info("=" * 40)
    
    if fix_syntax_errors():
        logger.info("✅ Correções aplicadas com sucesso!")
        logger.info("🧪 Testando sintaxe...")
        
        import subprocess
        result = subprocess.run(['python', '-m', 'py_compile', 'backend/main_enhanced.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("🎉 SINTAXE CORRIGIDA COM SUCESSO!")
            logger.info("💡 Agora você pode iniciar o servidor normalmente")
            return True
        else:
            logger.error("❌ Ainda há erros de sintaxe:")
            logger.error(result.stderr)
            return False
    else:
        logger.error("❌ Correção falhou")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)