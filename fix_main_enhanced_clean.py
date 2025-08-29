#!/usr/bin/env python3
"""
Script para limpar e corrigir o arquivo main_enhanced.py
"""

import os
import re

def fix_main_enhanced():
    """Corrige o arquivo main_enhanced.py removendo duplicações e aplicando a correção correta"""
    
    main_file = "backend/main_enhanced.py"
    
    if not os.path.exists(main_file):
        print(f"❌ Arquivo {main_file} não encontrado")
        return False
    
    # Ler o arquivo original
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup
    backup_file = f"{main_file}.backup_clean"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Backup criado: {backup_file}")
    
    # Método synthesize_speech corrigido
    corrected_method = '''    async def synthesize_speech(self, text: str, voice: str = "", 
        language: str = "", engine: str = "") -> dict:
        """
        Synthesize speech from text with proper speaker and language handling
        """
        logger.info(f"🔊 TTS Request: '{text[:50]}...' | Voice: {voice} | Language: {language} | Engine: {engine}")
        
        # Use Coqui TTS if available and requested
        if self.coqui_tts and engine in ["coqui", None]:
            try:
                import tempfile
                import base64
                
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                temp_path = temp_file.name
                temp_file.close()
                
                # Check if this is a cloned voice request
                is_cloned_voice = voice and voice.startswith("cloned_")
                
                # Determine model capabilities
                model_name = self.current_model or ""
                is_multi_speaker = hasattr(self.coqui_tts.tts, 'speakers') and self.coqui_tts.tts.speakers
                is_multi_lingual = hasattr(self.coqui_tts.tts, 'language_manager') and self.coqui_tts.tts.language_manager
                
                logger.info(f"🔍 Model analysis:")
                logger.info(f"   Model: {model_name}")
                logger.info(f"   Multi-speaker: {is_multi_speaker}")
                logger.info(f"   Multi-lingual: {is_multi_lingual}")
                
                if is_cloned_voice:
                    cloned_voice_name = voice.replace("cloned_", "")
                    ref_audio_dir = "reference_audio"
                    ref_audio_path = None
                    
                    # Look for reference audio
                    if os.path.exists(ref_audio_dir):
                        for filename in os.listdir(ref_audio_dir):
                            if cloned_voice_name.lower() in filename.lower() and filename.endswith(('.wav', '.mp3', '.flac')):
                                ref_audio_path = os.path.join(ref_audio_dir, filename)
                                break
                    
                    if ref_audio_path and os.path.exists(ref_audio_path):
                        logger.info(f"🎵 Using reference audio: {ref_audio_path}")
                        
                        # Prepare synthesis parameters for voice cloning
                        synthesis_params = {
                            "text": text,
                            "file_path": temp_path,
                            "speaker_wav": ref_audio_path
                        }
                        
                        # Add language only if model supports it
                        if is_multi_lingual:
                            synthesis_params["language"] = "pt"
                        
                        self.coqui_tts.tts_to_file(**synthesis_params)
                        
                    else:
                        logger.warning(f"⚠️ No reference audio found for cloned voice '{cloned_voice_name}'")
                        
                        # Fallback synthesis parameters
                        synthesis_params = {
                            "text": text,
                            "file_path": temp_path
                        }
                        
                        # Add speaker if model is multi-speaker
                        if is_multi_speaker:
                            speaker = self.coqui_tts.tts.speakers[0]
                            synthesis_params["speaker"] = speaker
                            logger.info(f"🎤 Using default speaker: {speaker}")
                        
                        # Add language only if model supports it
                        if is_multi_lingual:
                            synthesis_params["language"] = "pt"
                        
                        self.coqui_tts.tts_to_file(**synthesis_params)
                else:
                    # Regular synthesis
                    synthesis_params = {
                        "text": text,
                        "file_path": temp_path
                    }
                    
                    # Add speaker if model is multi-speaker
                    if is_multi_speaker:
                        speaker = self.coqui_tts.tts.speakers[0]
                        synthesis_params["speaker"] = speaker
                        logger.info(f"🎤 Using speaker: {speaker}")
                    
                    # Add language only if model supports it
                    if is_multi_lingual:
                        language_code = "pt" if "pt" in (language or "").lower() else "en"
                        synthesis_params["language"] = language_code
                    
                    logger.info(f"🔊 Synthesis parameters: {list(synthesis_params.keys())}")
                    self.coqui_tts.tts_to_file(**synthesis_params)
                
                # Read audio data
                with open(temp_path, 'rb') as f:
                    audio_data = f.read()
                
                # Cleanup
                os.unlink(temp_path)
                
                # Encode to base64 for transfer
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                method_name = f"coqui_tts_cloned_{cloned_voice_name}" if is_cloned_voice else f"coqui_tts_{self.current_model}"
                
                return {
                    "success": True,
                    "message": f"TTS generated with {'cloned voice' if is_cloned_voice else f'Coqui TTS ({self.current_model})'}",
                    "text": text,
                    "voice": voice,
                    "language": language,
                    "engine": engine,
                    "audio_size": len(audio_data),
                    "duration": len(text) / 10,
                    "audio_data": audio_base64,
                    "method": method_name
                }
                
            except Exception as coqui_error:
                logger.error(f"Coqui TTS failed: {coqui_error}")
                return {"success": False, "error": f"Coqui TTS failed: {str(coqui_error)}"}
        
        elif engine == "coqui":
            # Coqui was requested but is not available
            logger.error("Coqui TTS requested but not available - this is likely due to MeCab issues on Windows")
            return {"success": False, "error": "Coqui TTS not available"}'''
    
    # Encontrar e remover métodos duplicados/problemáticos
    lines = content.split('\n')
    new_lines = []
    skip_until_next_method = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Se encontramos o método synthesize_speech_original ou synthesize_speech_fixed
        if ('def synthesize_speech_original(' in line or 
            'def synthesize_speech_fixed(' in line or
            ('def synthesize_speech(' in line and 'async' in line)):
            
            if 'def synthesize_speech(' in line and 'async' in line:
                # Substituir pelo método corrigido
                method_lines = corrected_method.split('\n')
                for method_line in method_lines:
                    new_lines.append(method_line)
                new_lines.append('')
            
            # Pular até o próximo método
            method_indent = len(line) - len(line.lstrip())
            i += 1
            
            while i < len(lines):
                current_line = lines[i]
                current_indent = len(current_line) - len(current_line.lstrip())
                
                # Se encontramos uma linha com indentação igual ou menor que o método
                # e é uma definição de método/classe, saímos
                if (current_line.strip() and 
                    current_indent <= method_indent and 
                    ('def ' in current_line or 'class ' in current_line)):
                    break
                i += 1
            continue
        
        new_lines.append(line)
        i += 1
    
    # Escrever arquivo corrigido
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ Arquivo {main_file} corrigido com sucesso!")
    return True

def main():
    """Função principal"""
    print("🧹 Limpeza e Correção do main_enhanced.py")
    print("=" * 50)
    
    success = fix_main_enhanced()
    
    if success:
        print("\n✅ Correção aplicada com sucesso!")
        print("\n📋 Mudanças aplicadas:")
        print("1. ✅ Método synthesize_speech corrigido com detecção de capacidades do modelo")
        print("2. ✅ Uso correto de parâmetros speaker e language")
        print("3. ✅ Tratamento adequado de clonagem de voz")
        print("4. ✅ Remoção de métodos duplicados")
        
        print("\n🔄 Reinicie o servidor para aplicar as mudanças:")
        print("   python backend/main_enhanced.py")
    else:
        print("\n❌ Falha na correção")

if __name__ == "__main__":
    main()