@echo off
echo 🧪 TESTE FINAL SEM MECAB
echo =======================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Executando teste final...

python test_without_mecab.py

echo.
echo 💡 Se passou, o sistema está pronto!

pause