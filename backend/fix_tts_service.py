# Script to fix the TTSService.synthesize_speech method in main_enhanced.py
import re

# Read the file
with open('main_enhanced.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the correct synthesize_speech method
corrected_method = '''    async def synthesize_speech(self, text: str, voice: str = None, 
                               speed: float = 1.0, language: str = None, engine: str = None):
        """Synthesize speech from text with Coqui TTS support"""
        try:
            if not self.enabled:
                return {"success": True, "message": "TTS disabled", "audio_data": None}
            
            voice = voice or config.TTS_VOICE
            language = language or config.TTS_LANGUAGE
            engine = engine or "coqui"  # Default to Coqui TTS instead of gtts
            
            # Check if this is a cloned voice request
            is_cloned_voice = voice and (voice.startswith('cloned_') or voice.startswith('cloned:'))
            if is_cloned_voice:
                # Handle both formats of cloned voice naming
                if voice.startswith('cloned:'):
                    cloned_voice_name = voice.replace('cloned:', '')
                else:
                    cloned_voice_name = voice.replace('cloned_', '')
                logger.info(f"🎭 TTS: Using cloned voice '{cloned_voice_name}' for '{text[:50]}...'")
            else:
                logger.info(f"🔊 TTS: Synthesizing '{text[:50]}...' with {engine} engine and voice {voice}")
            
            # Engine selection logic - Force specific engine based on user choice
            if engine == "coqui" and self.coqui_tts:
                # Method 1: Coqui TTS (highest quality) - ONLY engine, no fallbacks
                try:
                    import tempfile
                    import base64
                    
                    # Generate speech with Coqui TTS
                    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    # Use Coqui TTS to generate audio
                    if is_cloned_voice:
                        # For cloned voices, we need to handle them properly
                        # Check if this is a YourTTS model that supports voice cloning
                        if hasattr(self.coqui_tts, 'is_multi_speaker') and self.coqui_tts.is_multi_speaker:
                            # Use speaker embedding for cloned voices
                            synthesis_text = text
                            # TODO: Implement proper speaker embedding loading for cloned voices
                        else:
                            # For other models, add a prefix to indicate it's a cloned voice
                            synthesis_text = f"[Cloned Voice: {cloned_voice_name}] {text}"
                    else:
                        synthesis_text = text
                        
                    self.coqui_tts.tts_to_file(text=synthesis_text, file_path=temp_path)
                    
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
                    # Return error instead of falling back
                    return {"success": False, "error": f"Coqui TTS failed: {str(coqui_error)}"}
            elif engine == "coqui":
                # Coqui was requested but is not available
                logger.error("Coqui TTS requested but not available")
                return {"success": False, "error": "Coqui TTS not available"}
            
            # Handle other engines without fallbacks
            elif engine == "pyttsx3":
                # Method 2: pyttsx3 (offline) - ONLY engine, no fallbacks
                try:
                    import pyttsx3
                    import base64
                    import tempfile
                    
                    engine_obj = pyttsx3.init()
                    
                    # Configure for Portuguese if available
                    voices = engine_obj.getProperty('voices')
                    if voices:
                        for v in voices:
                            if 'pt' in v.id.lower() or 'portuguese' in v.name.lower():
                                engine_obj.setProperty('voice', v.id)
                                break
                    
                    engine_obj.setProperty('rate', int(150 * speed))
                    engine_obj.setProperty('volume', 0.9)
                    
                    # For cloned voices, modify the text to indicate it's a simulation
                    if is_cloned_voice:
                        synthesis_text = f"Simulando voz clonada {cloned_voice_name}. {text}"
                    else:
                        synthesis_text = text
                    
                    # Generate speech to temp file
                    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    engine_obj.save_to_file(synthesis_text, temp_path)
                    engine_obj.runAndWait()
                    
                    # Read audio data
                    with open(temp_path, 'rb') as f:
                        audio_data = f.read()
                    
                    os.unlink(temp_path)  # Cleanup
                    
                    # Encode to base64
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    
                    method_name = f"pyttsx3_cloned_{cloned_voice_name}" if is_cloned_voice else "pyttsx3"
                    
                    return {
                        "success": True,
                        "message": f"TTS generated with {'cloned voice simulation' if is_cloned_voice else 'pyttsx3'}",
                        "text": text,
                        "voice": voice,
                        "language": language,
                        "engine": engine,
                        "audio_size": len(audio_data),
                        "duration": len(text) / 10,
                        "audio_data": audio_base64,
                        "method": method_name
                    }
                    
                except Exception as pyttsx3_error:
                    logger.error(f"pyttsx3 failed: {pyttsx3_error}")
                    return {"success": False, "error": f"pyttsx3 failed: {str(pyttsx3_error)}"}
            
            elif engine == "gtts":
                # Method 3: gTTS (online) - ONLY engine, no fallbacks
                try:
                    from gtts import gTTS
                    import tempfile
                    import base64
                    
                    lang_code = 'pt' if language.startswith('pt') else 'en'
                    
                    # Enhanced cloned voice simulation
                    if is_cloned_voice and hasattr(self, 'cloned_voice_simulation') and self.cloned_voice_simulation:
                        # Get cloned voice info for better simulation
                        cloned_voice_info = self._get_cloned_voice_info(cloned_voice_name)
                        voice_description = cloned_voice_info.get('description', f'voz clonada {cloned_voice_name}')
                        synthesis_text = f"Usando {voice_description}. {text}"
                        logger.info(f"🎭 Simulating cloned voice '{cloned_voice_name}' with gTTS")
                    elif is_cloned_voice:
                        synthesis_text = f"Simulando voz clonada {cloned_voice_name}. {text}"
                    else:
                        synthesis_text = text
                        
                    tts = gTTS(text=synthesis_text, lang=lang_code, slow=(speed < 1.0))
                    
                    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    tts.save(temp_path)
                    
                    with open(temp_path, 'rb') as f:
                        audio_data = f.read()
                    
                    os.unlink(temp_path)  # Cleanup
                    
                    # Encode to base64
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    
                    method_name = f"gTTS_cloned_{cloned_voice_name}" if is_cloned_voice else "gTTS"
                    
                    return {
                        "success": True,
                        "message": f"TTS generated with {'cloned voice simulation' if is_cloned_voice else 'Google TTS'}",
                        "text": text,
                        "voice": voice,
                        "language": language,
                        "engine": engine,
                        "audio_size": len(audio_data),
                        "duration": len(text) / 10,
                        "audio_data": audio_base64,
                        "method": method_name
                    }
                    
                except Exception as gtts_error:
                    logger.error(f"gTTS failed: {gtts_error}")
                    return {"success": False, "error": f"gTTS failed: {str(gtts_error)}"}
            
            else:
                # Unknown engine
                return {"success": False, "error": f"Unknown TTS engine: {engine}"}
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return {"success": False, "error": str(e)}'''

# Find and replace the problematic method
# Look for the start of the synthesize_speech method
pattern = r'(    async def synthesize_speech\(.*?^\s*except Exception as e:.*?logger\.error\(f"TTS error: {e}"\).*?return {"success": False, "error": str\(e\)}\n\s*\})'
# Use re.DOTALL to match across multiple lines
match = re.search(pattern, content, re.DOTALL | re.MULTILINE)

if match:
    # Replace the problematic method with the corrected one
    content = content[:match.start()] + corrected_method + content[match.end():]
    
    # Write the fixed content back to the file
    with open('main_enhanced.py', 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    print("TTSService.synthesize_speech method fixed successfully!")
else:
    print("Could not find the synthesize_speech method to fix.")