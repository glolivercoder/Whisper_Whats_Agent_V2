@echo off
echo 🔧 REMOVENDO MECAB COMPLETAMENTE
echo ================================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!

echo 🗑️ Removendo MeCab do ambiente virtual...
pip uninstall mecab-python3 -y

echo 🗑️ Removendo dependências relacionadas...
pip uninstall unidic -y

echo 📦 Instalando TTS sem dependências japonesas...
pip install TTS --no-deps --force-reinstall

echo 📦 Reinstalando dependências necessárias (sem MeCab)...
pip install torch torchaudio transformers==4.31.0 tokenizers==0.13.3
pip install soundfile librosa numpy scipy
pip install flask fastapi uvicorn
pip install aiohttp requests pyyaml

echo.
echo 🧪 Testando TTS sem MeCab...
python -c "
import os
os.environ['COQUI_TOS_AGREED'] = '1'
os.environ['PYTHONWARNINGS'] = 'ignore'

try:
    print('🔄 Importando TTS...')
    from TTS.api import TTS
    print('✅ TTS importado sem MeCab!')
    
    print('🔄 Carregando XTTS v2...')
    tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
    print('✅ XTTS v2 carregado!')
    
    print('🎉 SUCESSO! MeCab removido e TTS funcionando!')
    
except Exception as e:
    print(f'❌ Erro: {e}')
"

echo.
echo 💡 Se funcionou, execute: start_enhanced_correct.bat

pause