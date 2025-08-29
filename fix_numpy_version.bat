@echo off
echo 🔧 CORRIGINDO VERSÃO DO NUMPY
echo =============================

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo ✅ Ambiente virtual ativado!
echo 🔄 Corrigindo versão do NumPy...

echo 📦 Instalando NumPy compatível...
pip install "numpy<2.0" --force-reinstall

echo 📦 Verificando versões...
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import numba; print('Numba:', numba.__version__)"

echo.
echo 🧪 Testando XTTS v2 novamente...
python -c "
import os
os.environ['COQUI_TOS_AGREED'] = '1'
os.environ['COQUI_TTS_NO_MECAB'] = '1'
os.environ['PYTHONWARNINGS'] = 'ignore'

try:
    from TTS.api import TTS
    print('✅ TTS importado')
    
    tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
    print('✅ XTTS v2 carregado com sucesso!')
    
    if hasattr(tts, 'tts_to_file'):
        print('✅ Método tts_to_file disponível')
        print('🎉 TUDO FUNCIONANDO!')
    else:
        print('❌ Método tts_to_file não encontrado')
        
except Exception as e:
    print(f'❌ Erro: {e}')
"

echo.
echo 💡 Se funcionou, execute: start_enhanced_correct.bat

pause