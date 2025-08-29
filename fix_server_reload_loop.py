#!/usr/bin/env python3
"""
FIX DO LOOP DE RECARREGAMENTO DO SERVIDOR
=========================================

Corrige o problema de loop infinito de recarregamento do servidor
causado pelo watchfiles detectando mudanças constantemente.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_reload_loop():
    """Corrige o loop de recarregamento do servidor"""
    
    main_file = "backend/main_enhanced.py"
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info("🔄 Corrigindo configuração do uvicorn...")
        
        # Encontrar a configuração do uvicorn
        uvicorn_start = content.find('uvicorn.run(')
        if uvicorn_start == -1:
            logger.error("❌ Configuração uvicorn.run não encontrada")
            return False
        
        # Encontrar o final da configuração
        uvicorn_section = content[uvicorn_start:]
        closing_paren = uvicorn_section.find(')')
        if closing_paren == -1:
            logger.error("❌ Final da configuração uvicorn não encontrado")
            return False
        
        # Nova configuração do uvicorn (sem reload em produção)
        new_uvicorn_config = '''uvicorn.run(
        "main_enhanced:app",
        host="0.0.0.0",
        port=8001,
        reload=False,  # Disabled to prevent reload loops
        log_level="info",
        access_log=False  # Reduce log noise
    )'''
        
        # Substituir a configuração
        uvicorn_end = uvicorn_start + closing_paren + 1
        new_content = (
            content[:uvicorn_start] + 
            new_uvicorn_config + 
            content[uvicorn_end:]
        )
        
        # Salvar o arquivo corrigido
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info("✅ Configuração uvicorn corrigida (reload=False)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao corrigir configuração uvicorn: {e}")
        return False

def fix_database_initialization():
    """Corrige problemas de inicialização do banco de dados"""
    
    main_file = "backend/main_enhanced.py"
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info("🔄 Corrigindo inicialização do banco de dados...")
        
        # Procurar pela classe DatabaseService
        db_service_start = content.find('class DatabaseService:')
        if db_service_start == -1:
            logger.error("❌ Classe DatabaseService não encontrada")
            return False
        
        # Procurar pelo método __init__ da DatabaseService
        init_start = content.find('def __init__(self', db_service_start)
        if init_start == -1:
            logger.error("❌ Método __init__ da DatabaseService não encontrado")
            return False
        
        # Verificar se já tem lazy_load
        if 'lazy_load' in content[db_service_start:db_service_start+2000]:
            logger.info("✅ DatabaseService já tem lazy_load configurado")
            return True
        
        # Encontrar a linha de inicialização do DatabaseService
        db_init_pattern = 'db_service = DatabaseService()'
        if db_init_pattern in content:
            # Substituir por versão com lazy loading
            new_content = content.replace(
                db_init_pattern,
                'db_service = DatabaseService(lazy_load=True)  # Enable lazy loading to reduce startup overhead'
            )
            
            # Salvar o arquivo corrigido
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            logger.info("✅ DatabaseService configurado com lazy loading")
            return True
        else:
            logger.warning("⚠️ Padrão de inicialização DatabaseService não encontrado")
            return False
        
    except Exception as e:
        logger.error(f"❌ Erro ao corrigir DatabaseService: {e}")
        return False

def add_production_mode():
    """Adiciona modo de produção para reduzir logs e melhorar performance"""
    
    main_file = "backend/main_enhanced.py"
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info("🔄 Adicionando modo de produção...")
        
        # Verificar se já tem configuração de produção
        if 'PRODUCTION_MODE' in content:
            logger.info("✅ Modo de produção já configurado")
            return True
        
        # Encontrar onde adicionar a configuração (após os imports)
        import_end = content.find('# Configuration Management')
        if import_end == -1:
            import_end = content.find('class Config:')
        
        if import_end == -1:
            logger.error("❌ Local para adicionar configuração não encontrado")
            return False
        
        # Configuração de produção
        production_config = '''
# Production mode configuration
PRODUCTION_MODE = os.getenv("PRODUCTION_MODE", "true").lower() == "true"

# Reduce logging in production
if PRODUCTION_MODE:
    import logging
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)

'''
        
        # Inserir a configuração
        new_content = content[:import_end] + production_config + content[import_end:]
        
        # Salvar o arquivo corrigido
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info("✅ Modo de produção adicionado")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao adicionar modo de produção: {e}")
        return False

def create_production_startup_script():
    """Cria script de inicialização para produção"""
    
    script_content = '''@echo off
title WhatsApp Voice Agent V2 Enhanced - Production Mode
color 0A

echo ========================================
echo  🚀 WhatsApp Voice Agent V2 Enhanced
echo  🏭 PRODUCTION MODE - Stable Server
echo  📍 Starting Server on Port 8001
echo ========================================
echo.

:: Navigate to project directory
cd /d "%~dp0"

:: Set production environment
set PRODUCTION_MODE=true
set COQUI_TOS_AGREED=1
set COQUI_TTS_NO_MECAB=1
set PYTHONPATH=%CD%

:: Check if virtual environment exists
if exist "venv\\Scripts\\activate.bat" (
    echo ✅ Virtual environment found
    echo 🔄 Activating virtual environment...
    call venv\\Scripts\\activate.bat
) else (
    echo ⚠️  Virtual environment not found - using system Python
)

echo.
echo 🛑 Stopping any existing servers...
taskkill /f /im python.exe >nul 2>&1
for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":8001 "') do taskkill /f /pid %%i >nul 2>&1

echo ⏳ Waiting for cleanup...
timeout /t 2 /nobreak >nul

echo.
echo 🚀 Starting Production Server...
echo ========================================
echo 📍 Main URL: http://localhost:8001
echo 📖 API Docs: http://localhost:8001/docs
echo 🔍 Health Check: http://localhost:8001/health
echo.
echo ✅ PRODUCTION FEATURES:
echo   • No auto-reload (stable)
echo   • Reduced logging
echo   • Optimized performance
echo   • Database lazy loading
echo.

cd backend
python main_enhanced.py

echo.
echo 🛑 Server stopped. Press any key to exit...
pause
'''
    
    try:
        with open('start_production.bat', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        logger.info("✅ Script de produção criado: start_production.bat")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar script de produção: {e}")
        return False

def main():
    """Executa todas as correções"""
    logger.info("🔧 CORRIGINDO LOOP DE RECARREGAMENTO DO SERVIDOR")
    logger.info("=" * 55)
    
    fixes = [
        ("Configuração Uvicorn", fix_reload_loop),
        ("Inicialização Database", fix_database_initialization),
        ("Modo Produção", add_production_mode),
        ("Script Produção", create_production_startup_script)
    ]
    
    success_count = 0
    
    for fix_name, fix_func in fixes:
        logger.info(f"🔄 Aplicando: {fix_name}")
        
        try:
            if fix_func():
                logger.info(f"✅ {fix_name}: Aplicado com sucesso")
                success_count += 1
            else:
                logger.error(f"❌ {fix_name}: Falhou")
        except Exception as e:
            logger.error(f"❌ {fix_name}: Erro - {e}")
    
    # Resultado final
    logger.info("=" * 55)
    logger.info(f"📊 RESULTADO: {success_count}/{len(fixes)} correções aplicadas")
    
    if success_count >= 3:  # Pelo menos as correções principais
        logger.info("🎉 CORREÇÕES PRINCIPAIS APLICADAS COM SUCESSO!")
        logger.info("")
        logger.info("💡 OPÇÕES PARA INICIAR O SERVIDOR:")
        logger.info("   1. Modo Produção (recomendado): start_production.bat")
        logger.info("   2. Modo Normal: ./start_enhanced_correct.bat")
        logger.info("")
        logger.info("🏭 O modo produção oferece:")
        logger.info("   • Sem auto-reload (mais estável)")
        logger.info("   • Logs reduzidos")
        logger.info("   • Melhor performance")
        return True
    else:
        logger.warning("⚠️ Algumas correções falharam")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)