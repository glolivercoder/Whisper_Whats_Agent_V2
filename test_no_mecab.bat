@echo off
echo 🔧 TESTANDO XTTS v2 SEM MECAB
echo =============================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Executando solução sem MeCab...

python fix_xtts_no_mecab.py

echo.
echo 💡 Se funcionou, o servidor deve funcionar agora
echo 💡 Execute: start_enhanced_correct.bat

pause