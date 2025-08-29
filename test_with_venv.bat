@echo off
echo 🧪 TESTANDO DEPENDÊNCIAS NO AMBIENTE VIRTUAL
echo =============================================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Executando teste...

python test_venv_dependencies.py

echo.
echo 💡 Mantenha o ambiente virtual ativo para usar o servidor
echo 💡 Use 'deactivate' para sair do venv

pause