@echo off
echo 🔧 CORRIGINDO ERRO BASE64
echo ========================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Corrigindo erro da variável base64...

python fix_base64_error.py

echo.
echo 💡 Se funcionou, teste o servidor agora

pause