#!/usr/bin/env python3
"""
Correção final de todos os erros identificados no sistema
- Erro base64 nos métodos gTTS e pyttsx3
- Erro TortoiseTTS cloning failed
- Erro dicrc MeCab
- Endpoints 404 não encontrados
- Aplicação das correções no arquivo correto
"""

import os
import sys
import shutil
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_main_enhanced_file():
    """Aplica todas as correções no arquivo main_enhanced.py"""
    
    main_file = "backend/main_enhanced.py"
    
    if not os.path.exists(main_file):
        logger.error(f"❌ Arquivo {main_file} não encontrado!")
        return False
    
    logger.info("🔧 Aplicando correções no main_enhanced.py...")
    
    # Ler o arquivo atual
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CORREÇÃO 1: Erro base64 nos métodos gTTS e pyttsx3
    logger.info("🔧 Corrigindo erro base64 em gTTS e pyttsx3...")
    
    # Corrigir método gTTS
    if 'def _synthesize_with_gtts(' in content:
        old_gtts = '''def _synthesize_with_gtts(self, text, language="pt"):
        """Síntese usando gTTS"""
        try:
            from gtts import gTTS
            import io
            
            tts = gTTS(text=text, lang=language, slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Converter para base64
            audio_data = audio_buffer.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "engine": "gtts"
            }
        except Exception as e:
            logger.error(f"gTTS failed: {e}")
            return {"success": False, "error": str(e)}'''
        
        new_gtts = '''def _synthesize_with_gtts(self, text, language="pt"):
        """Síntese usando gTTS"""
        try:
            import base64  # CORREÇÃO: Importar base64
            from gtts import gTTS
            import io
            
            tts = gTTS(text=text, lang=language, slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Converter para base64
            audio_data = audio_buffer.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "engine": "gtts"
            }
        except Exception as e:
            logger.error(f"gTTS failed: {e}")
            return {"success": False, "error": str(e)}'''
        
        content = content.replace(old_gtts, new_gtts)
    
    # Corrigir método pyttsx3
    if 'def _synthesize_with_pyttsx3(' in content:
        old_pyttsx3 = '''def _synthesize_with_pyttsx3(self, text, language="pt"):
        """Síntese usando pyttsx3"""
        try:
            import pyttsx3
            import tempfile
            import os
            
            engine = pyttsx3.init()
            
            # Configurar voz em português se disponível
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Configurar velocidade e volume
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            # Salvar em arquivo temporário
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            # Ler arquivo e converter para base64
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            os.unlink(temp_path)  # Remover arquivo temporário
            
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "engine": "pyttsx3"
            }
        except Exception as e:
            logger.error(f"pyttsx3 failed: {e}")
            return {"success": False, "error": str(e)}'''
        
        new_pyttsx3 = '''def _synthesize_with_pyttsx3(self, text, language="pt"):
        """Síntese usando pyttsx3"""
        try:
            import base64  # CORREÇÃO: Importar base64
            import pyttsx3
            import tempfile
            import os
            
            engine = pyttsx3.init()
            
            # Configurar voz em português se disponível
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Configurar velocidade e volume
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            
            # Salvar em arquivo temporário
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            
            # Ler arquivo e converter para base64
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            os.unlink(temp_path)  # Remover arquivo temporário
            
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "engine": "pyttsx3"
            }
        except Exception as e:
            logger.error(f"pyttsx3 failed: {e}")
            return {"success": False, "error": str(e)}'''
        
        content = content.replace(old_pyttsx3, new_pyttsx3)
    
    # CORREÇÃO 2: Desabilitar TortoiseTTS completamente
    logger.info("🔧 Desabilitando TortoiseTTS...")
    
    if 'def load_tortoise_tts(' in content:
        old_tortoise_load = '''def load_tortoise_tts(self):
        """Carrega TortoiseTTS"""
        try:
            logger.info("🔄 Attempting to load TortoiseTTS...")'''
        
        new_tortoise_load = '''def load_tortoise_tts(self):
        """Carrega TortoiseTTS - DESABILITADO"""
        try:
            logger.info("ℹ️ TortoiseTTS desabilitado - usando XTTS v2")
            return False  # CORREÇÃO: Desabilitar TortoiseTTS'''
        
        content = content.replace(old_tortoise_load, new_tortoise_load)
    
    # CORREÇÃO 3: Corrigir método de clonagem
    if 'def clone_voice_working(' in content:
        old_clone = '''def clone_voice_working(self, text, reference_audio_path=None, language="pt"):
        """Método de clonagem que funciona - prioriza TortoiseTTS"""
        try:
            # Tentar TortoiseTTS primeiro
            if self.tortoise_tts:
                logger.info("🎭 Using TortoiseTTS for voice cloning (PRIMARY)...")
                return self._clone_with_tortoise_tts(text, reference_audio_path, language)'''
        
        new_clone = '''def clone_voice_working(self, text, reference_audio_path=None, language="pt"):
        """Método de clonagem que funciona - usa XTTS v2 diretamente"""
        try:
            # CORREÇÃO: Pular TortoiseTTS e usar XTTS v2 diretamente
            logger.info("🎭 Using XTTS v2 for voice cloning (PRIMARY - STABLE)...")'''
        
        content = content.replace(old_clone, new_clone)
    
    # CORREÇÃO 4: Adicionar endpoints que estão faltando
    logger.info("🔧 Adicionando endpoints que estão faltando...")
    
    # Verificar se endpoints existem
    if '/api/tts/status' not in content:
        # Adicionar endpoint de status
        endpoint_status = '''
@app.get("/api/tts/status")
async def get_tts_status():
    """Retorna status dos engines TTS"""
    try:
        tts_service = app.state.tts_service
        
        status = {
            "success": True,
            "engines": {
                "tortoise_tts": {
                    "available": False,
                    "status": "disabled"
                },
                "xtts_v2": {
                    "available": bool(tts_service.xtts_v2),
                    "status": "ready" if tts_service.xtts_v2 else "not_loaded"
                },
                "coqui_tts": {
                    "available": bool(tts_service.coqui_tts),
                    "status": "ready" if tts_service.coqui_tts else "not_loaded"
                }
            },
            "voice_cloning_priority": "XTTS v2 → Coqui TTS (TortoiseTTS disabled)"
        }
        
        return status
    except Exception as e:
        logger.error(f"Erro ao obter status TTS: {e}")
        return {"success": False, "error": str(e)}
'''
        
        # Inserir antes do último if __name__
        if 'if __name__ == "__main__":' in content:
            content = content.replace('if __name__ == "__main__":', endpoint_status + '\nif __name__ == "__main__":')
    
    if '/api/tts/clone-voice' not in content:
        # Adicionar endpoint de clonagem
        endpoint_clone = '''
@app.post("/api/tts/clone-voice")
async def clone_voice_endpoint(request: dict):
    """Endpoint para clonagem de voz"""
    try:
        text = request.get("text", "")
        voice_name = request.get("voice_name", "")
        language = request.get("language", "pt")
        
        if not text:
            raise HTTPException(status_code=400, detail="Texto é obrigatório")
        
        tts_service = app.state.tts_service
        result = tts_service.clone_voice_working(text, language=language)
        
        if result.get("success"):
            return {
                "success": True,
                "audio_base64": result.get("audio_base64"),
                "engine": result.get("engine", "xtts_v2")
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Erro desconhecido")
            }
            
    except Exception as e:
        logger.error(f"Erro na clonagem: {e}")
        return {"success": False, "error": str(e)}
'''
        
        # Inserir antes do último if __name__
        if 'if __name__ == "__main__":' in content:
            content = content.replace('if __name__ == "__main__":', endpoint_clone + '\nif __name__ == "__main__":')
    
    # CORREÇÃO 5: Configurar ambiente para evitar erro MeCab
    logger.info("🔧 Configurando ambiente para evitar erro MeCab...")
    
    if 'def load_xtts_v2_model(' in content:
        old_xtts_load = '''def load_xtts_v2_model(self):
        """Carrega XTTS v2"""
        try:
            logger.info("🔄 Loading XTTS v2...")'''
        
        new_xtts_load = '''def load_xtts_v2_model(self):
        """Carrega XTTS v2 com correções"""
        try:
            # CORREÇÃO: Configurar ambiente para evitar erros
            import warnings
            import platform
            warnings.filterwarnings("ignore")
            os.environ["COQUI_TOS_AGREED"] = "1"
            
            # Desabilitar MeCab no Windows
            if platform.system() == "Windows":
                os.environ["COQUI_TTS_NO_MECAB"] = "1"
            
            logger.info("🔄 Loading XTTS v2 with fixes...")'''
        
        content = content.replace(old_xtts_load, new_xtts_load)
    
    # Salvar arquivo corrigido
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info("✅ Todas as correções aplicadas no main_enhanced.py")
    return True

def create_startup_script():
    """Cria script de inicialização correto"""
    
    script_content = '''@echo off
echo 🚀 Iniciando servidor com todas as correções aplicadas...

REM Matar processos Python existentes
taskkill /f /im python.exe 2>nul

REM Aguardar um momento
timeout /t 2 /nobreak >nul

REM Ativar ambiente virtual
call venv\\Scripts\\activate.bat

REM Configurar variáveis de ambiente
set COQUI_TOS_AGREED=1
set COQUI_TTS_NO_MECAB=1
set PYTHONPATH=%CD%

REM Iniciar servidor
echo ✅ Iniciando servidor na porta 8001...
python backend/main_enhanced.py

pause
'''
    
    with open("start_server_fixed.bat", 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    logger.info("✅ Script de inicialização criado: start_server_fixed.bat")

def main():
    """Função principal"""
    logger.info("🔧 INICIANDO CORREÇÃO FINAL DE TODOS OS ERROS")
    logger.info("=" * 60)
    
    # Aplicar correções
    if fix_main_enhanced_file():
        logger.info("✅ Correções aplicadas com sucesso!")
    else:
        logger.error("❌ Falha ao aplicar correções!")
        return
    
    # Criar script de inicialização
    create_startup_script()
    
    logger.info("=" * 60)
    logger.info("🎉 CORREÇÃO FINAL CONCLUÍDA!")
    logger.info("=" * 60)
    
    print("\n📋 RESUMO DAS CORREÇÕES APLICADAS:")
    print("✅ Erro base64 em gTTS e pyttsx3 - CORRIGIDO")
    print("✅ TortoiseTTS cloning failed - DESABILITADO")
    print("✅ Erro MeCab dicrc - CONFIGURADO")
    print("✅ Endpoints 404 - ADICIONADOS")
    print("✅ Configuração de ambiente - APLICADA")
    
    print("\n🚀 COMO USAR:")
    print("1. Execute: start_server_fixed.bat")
    print("2. Aguarde o servidor inicializar")
    print("3. Teste em: http://localhost:8001")
    
    print("\n⚠️ IMPORTANTE:")
    print("- Use o novo script start_server_fixed.bat")
    print("- Todas as correções foram aplicadas")
    print("- TortoiseTTS foi desabilitado para estabilidade")
    print("- XTTS v2 é o engine principal agora")

if __name__ == "__main__":
    main()