@echo off
echo 🔧 CORRIGINDO MECAB E TESTANDO XTTS v2
echo =====================================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Executando correção do MeCab...

python fix_mecab_complete.py

echo.
echo 💡 Se funcionou, execute: start_enhanced_correct.bat
echo 💡 Mantenha o ambiente virtual ativo

pause