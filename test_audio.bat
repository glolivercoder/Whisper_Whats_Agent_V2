@echo off
echo 🧪 TESTE FINAL DA GERAÇÃO DE ÁUDIO
echo ==================================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Testando geração de áudio...

python test_audio_generation.py

echo.
echo 💡 Se funcionou, o sistema está pronto!

pause