@echo off
echo 🔧 INSTALANDO DEPENDÊNCIAS NO AMBIENTE VIRTUAL
echo ================================================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 📍 Verificando Python atual...
python -c "import sys; print('Python path:', sys.executable)"

echo.
echo 🔄 Instalando dependências específicas para XTTS v2...
echo ================================================

echo 📦 Instalando PyTorch específico...
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cpu

echo 📦 Instalando Transformers específico...
pip install transformers==4.30.0

echo 📦 Instalando TTS (Coqui)...
pip install TTS

echo 📦 Instalando dependências adicionais...
pip install soundfile librosa numpy scipy tokenizers

echo.
echo ✅ INSTALAÇÃO CONCLUÍDA!
echo ================================================
echo 🎯 Dependências instaladas no ambiente virtual
echo 💡 Use 'venv\Scripts\activate.bat' para ativar o venv
echo 🚀 Execute 'start_enhanced_correct.bat' para testar

pause