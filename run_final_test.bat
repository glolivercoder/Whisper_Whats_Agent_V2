@echo off
echo 🧪 TESTE FINAL DO SETUP
echo ====================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Executando teste final...

python test_final_fix.py

echo.
echo 💡 Se passou, execute: start_enhanced_correct.bat

pause