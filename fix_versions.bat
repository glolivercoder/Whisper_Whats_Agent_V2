@echo off
echo 🔧 CORRIGINDO VERSÕES DAS DEPENDÊNCIAS
echo =====================================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Corrigindo versões das dependências...

python fix_transformers_version.py

echo.
echo 💡 Se funcionou, teste o servidor agora
echo 💡 Execute: start_enhanced_correct.bat

pause