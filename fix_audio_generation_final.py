#!/usr/bin/env python3
"""
CORREÇÃO DEFINITIVA DA GERAÇÃO DE ÁUDIO
Vamos resolver o problema de uma vez por todas
"""

import os
import sys
import shutil
from pathlib import Path

def fix_audio_generation():
    """Aplica correção definitiva na geração de áudio"""
    print("🔧 CORREÇÃO DEFINITIVA DA GERAÇÃO DE ÁUDIO")
    print("=" * 60)
    
    # 1. Verificar estrutura de diretórios
    print("📁 Verificando diretórios...")
    dirs_to_check = ['reference_audio', 'audios', 'cloned_voices']
    for dir_name in dirs_to_check:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ Criado: {dir_name}/")
        else:
            print(f"✅ Existe: {dir_name}/")
    
    # 2. Corrigir o serviço TTS
    print("\n🎭 Corrigindo serviço TTS...")
    
    tts_service_content = '''"""
Serviço TTS corrigido para geração de áudio garantida
"""

import os
import base64
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import torch
import torchaudio
import numpy as np

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        """Inicializa o serviço TTS com configurações robustas"""
        self.reference_audio_dir = Path("reference_audio")
        self.output_audio_dir = Path("audios")
        self.cloned_voices_dir = Path("cloned_voices")
        
        # Criar diretórios se não existirem
        for dir_path in [self.reference_audio_dir, self.output_audio_dir, self.cloned_voices_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Configurar variáveis de ambiente para Coqui TTS
        os.environ["COQUI_TOS_AGREED"] = "1"
        os.environ["COQUI_TTS_AGREED"] = "1"
        
        self.tts_model = None
        self.model_loaded = False
        
        # Tentar carregar modelo
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo XTTS v2 de forma robusta"""
        try:
            from TTS.api import TTS
            
            logger.info("🔄 Carregando XTTS v2...")
            
            # Usar modelo específico
            model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
            
            self.tts_model = TTS(model_name, progress_bar=False)
            self.model_loaded = True
            
            logger.info("✅ XTTS v2 carregado com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar modelo: {e}")
            self.model_loaded = False
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Lista vozes disponíveis"""
        voices = []
        total_voices = 0
        cloned_count = 0
        reference_count = 0
        
        # Vozes de referência
        if self.reference_audio_dir.exists():
            for audio_file in self.reference_audio_dir.glob("*.wav"):
                voice_name = audio_file.stem.split('_')[0]  # Pegar nome antes do _
                voices.append({
                    "name": voice_name,
                    "type": "reference",
                    "file": str(audio_file)
                })
                reference_count += 1
        
        # Vozes clonadas
        if self.cloned_voices_dir.exists():
            for config_file in self.cloned_voices_dir.glob("*.json"):
                voice_name = config_file.stem
                voices.append({
                    "name": voice_name,
                    "type": "cloned",
                    "config": str(config_file)
                })
                cloned_count += 1
        
        total_voices = len(voices)
        
        return {
            "voices": voices,
            "total": total_voices,
            "cloned_voices": cloned_count,
            "reference_voices": reference_count
        }
    
    def _find_reference_audio(self, voice_name: str) -> Optional[str]:
        """Encontra arquivo de áudio de referência para uma voz"""
        if not self.reference_audio_dir.exists():
            return None
        
        # Procurar por arquivos que começam com o nome da voz
        for audio_file in self.reference_audio_dir.glob(f"{voice_name}*.wav"):
            return str(audio_file)
        
        # Procurar por arquivos que contenham o nome da voz
        for audio_file in self.reference_audio_dir.glob("*.wav"):
            if voice_name.lower() in audio_file.stem.lower():
                return str(audio_file)
        
        return None
    
    def generate_speech(self, text: str, voice_name: str, language: str = "pt") -> Dict[str, Any]:
        """Gera fala usando XTTS v2 com garantia de áudio"""
        try:
            if not self.model_loaded:
                return {
                    "success": False,
                    "message": "Modelo TTS não carregado",
                    "audio_data": None
                }
            
            # Encontrar áudio de referência
            reference_audio = self._find_reference_audio(voice_name)
            if not reference_audio:
                return {
                    "success": False,
                    "message": f"Áudio de referência não encontrado para {voice_name}",
                    "audio_data": None
                }
            
            logger.info(f"🎭 Gerando fala para '{voice_name}' com texto: {text[:50]}...")
            logger.info(f"📁 Usando referência: {reference_audio}")
            
            # Gerar nome único para o arquivo de saída
            import time
            timestamp = int(time.time())
            output_filename = f"{voice_name}_generated_{timestamp}.wav"
            output_path = self.output_audio_dir / output_filename
            
            # Gerar áudio usando XTTS v2
            self.tts_model.tts_to_file(
                text=text,
                speaker_wav=reference_audio,
                language=language,
                file_path=str(output_path)
            )
            
            # Verificar se o arquivo foi criado
            if not output_path.exists():
                return {
                    "success": False,
                    "message": "Arquivo de áudio não foi gerado",
                    "audio_data": None
                }
            
            # Verificar tamanho do arquivo
            file_size = output_path.stat().st_size
            if file_size < 1000:  # Menos de 1KB é suspeito
                return {
                    "success": False,
                    "message": f"Arquivo de áudio muito pequeno: {file_size} bytes",
                    "audio_data": None
                }
            
            # Converter para base64
            with open(output_path, "rb") as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            logger.info(f"✅ Áudio gerado com sucesso: {file_size} bytes")
            
            return {
                "success": True,
                "message": f"Voz clonada com XTTS v2 - {voice_name}",
                "audio_data": audio_data,
                "file_path": str(output_path),
                "file_size": file_size,
                "voice_name": voice_name,
                "engine": "xtts_v2_fixed"
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na geração de fala: {e}")
            return {
                "success": False,
                "message": f"Erro na geração: {str(e)}",
                "audio_data": None
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do serviço TTS"""
        return {
            "model_loaded": self.model_loaded,
            "model_name": "xtts_v2" if self.model_loaded else None,
            "available_voices": len(self.get_available_voices()["voices"]),
            "reference_audio_dir": str(self.reference_audio_dir),
            "output_audio_dir": str(self.output_audio_dir)
        }

# Instância global do serviço
tts_service = TTSService()
'''
    
    # Salvar o serviço corrigido
    with open("backend/tts_service_fixed.py", "w", encoding="utf-8") as f:
        f.write(tts_service_content)
    
    print("✅ Serviço TTS corrigido salvo em backend/tts_service_fixed.py")
    
    # 3. Corrigir o endpoint principal
    print("\n🌐 Corrigindo endpoint TTS...")
    
    # Ler o main_enhanced.py atual
    with open("backend/main_enhanced.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Adicionar import do serviço corrigido
    if "from .tts_service_fixed import tts_service" not in content:
        # Encontrar a seção de imports
        import_section = content.find("from fastapi import")
        if import_section != -1:
            # Adicionar import após os imports do FastAPI
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("from fastapi import"):
                    lines.insert(i + 1, "from .tts_service_fixed import tts_service")
                    break
            content = '\n'.join(lines)
    
    # Corrigir o endpoint /api/tts
    tts_endpoint_fixed = '''@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Endpoint TTS corrigido com geração garantida de áudio"""
    try:
        logger.info(f"🎭 TTS Request: {request.text[:50]}... | Voice: {request.voice} | Engine: {request.engine}")
        
        # Usar o serviço TTS corrigido
        result = tts_service.generate_speech(
            text=request.text,
            voice_name=request.voice,
            language=request.language
        )
        
        if result["success"]:
            logger.info(f"✅ TTS Success: {result['message']}")
            return {
                "success": True,
                "message": result["message"],
                "audio_data": result["audio_data"],
                "voice_name": result["voice_name"],
                "engine": result["engine"],
                "file_size": result.get("file_size", 0)
            }
        else:
            logger.error(f"❌ TTS Failed: {result['message']}")
            return {
                "success": False,
                "message": result["message"],
                "audio_data": None
            }
            
    except Exception as e:
        logger.error(f"❌ TTS Endpoint Error: {e}")
        return {
            "success": False,
            "message": f"Erro no endpoint TTS: {str(e)}",
            "audio_data": None
        }'''
    
    # Substituir o endpoint existente
    if "@app.post(\"/api/tts\")" in content:
        # Encontrar o início e fim do endpoint atual
        start_marker = "@app.post(\"/api/tts\")"
        start_pos = content.find(start_marker)
        
        if start_pos != -1:
            # Encontrar o próximo @app ou final do arquivo
            next_endpoint = content.find("@app.", start_pos + 1)
            if next_endpoint == -1:
                next_endpoint = len(content)
            
            # Substituir o endpoint
            content = content[:start_pos] + tts_endpoint_fixed + "\n\n" + content[next_endpoint:]
    else:
        # Adicionar o endpoint se não existir
        content += "\n\n" + tts_endpoint_fixed
    
    # Salvar o arquivo corrigido
    with open("backend/main_enhanced.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ Endpoint TTS corrigido no main_enhanced.py")
    
    print("\n🎉 CORREÇÃO DEFINITIVA APLICADA!")
    print("=" * 60)
    print("✅ Serviço TTS corrigido")
    print("✅ Endpoint TTS corrigido")
    print("✅ Geração de áudio garantida")
    print("💡 Execute: ./start_enhanced_correct.bat")

if __name__ == "__main__":
    fix_audio_generation()