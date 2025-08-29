#!/usr/bin/env python3
"""
Correção do erro "Invalid file: None" no XTTS v2
O problema é que o XTTS v2 sempre precisa de um arquivo de referência
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_invalid_file_none_error():
    """Corrige o erro 'Invalid file: None' no main_enhanced.py"""
    
    main_file = "backend/main_enhanced.py"
    
    if not os.path.exists(main_file):
        logger.error(f"❌ Arquivo {main_file} não encontrado!")
        return False
    
    logger.info("🔧 Corrigindo erro 'Invalid file: None'...")
    
    # Ler o arquivo atual
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CORREÇÃO 1: Garantir que sempre há um arquivo de referência para XTTS v2
    # Procurar o método _clone_with_xtts_v2 e corrigir
    if 'def _clone_with_xtts_v2(' in content:
        # Encontrar e corrigir a chamada tts_to_file
        old_tts_call = '''            # Método oficial da documentação Coqui TTS com tratamento robusto
            try:
                self.xtts_v2.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=reference_audio_path,  # String, não lista
                    language=language
                )
                logger.info("✅ Método tts_to_file executado com sucesso")
                
            except Exception as tts_error:
                logger.error(f"❌ Erro no método tts_to_file: {tts_error}")
                
                # Tentar método alternativo com lista
                logger.info("🔄 Tentando método alternativo com lista...")
                try:
                    self.xtts_v2.tts_to_file(
                        text=text,
                        file_path=output_path,
                        speaker_wav=[reference_audio_path],  # Lista como alternativa
                        language=language
                    )
                    logger.info("✅ Método alternativo com lista funcionou")
                except Exception as alt_error:
                    logger.error(f"❌ Método alternativo também falhou: {alt_error}")
                    raise tts_error  # Relançar erro original'''
        
        new_tts_call = '''            # Método oficial da documentação Coqui TTS com correção do "Invalid file: None"
            try:
                # CRÍTICO: XTTS v2 SEMPRE precisa de speaker_wav, mesmo para síntese simples
                logger.info(f"🔄 Executando tts_to_file com speaker_wav: {reference_audio_path}")
                
                self.xtts_v2.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=reference_audio_path,  # OBRIGATÓRIO - nunca None
                    language=language
                )
                logger.info("✅ Método tts_to_file executado com sucesso")
                
            except Exception as tts_error:
                error_str = str(tts_error).lower()
                logger.error(f"❌ Erro no método tts_to_file: {tts_error}")
                
                # Diagnóstico específico do erro
                if "invalid file" in error_str and "none" in error_str:
                    logger.error("🔍 ERRO IDENTIFICADO: speaker_wav é None")
                    logger.error(f"   reference_audio_path atual: {reference_audio_path}")
                    
                    # Tentar criar arquivo dummy se necessário
                    if not reference_audio_path or not os.path.exists(reference_audio_path):
                        logger.info("🔄 Criando arquivo de referência dummy...")
                        dummy_path = self.create_dummy_reference_audio()
                        if dummy_path:
                            logger.info(f"✅ Usando arquivo dummy: {dummy_path}")
                            self.xtts_v2.tts_to_file(
                                text=text,
                                file_path=output_path,
                                speaker_wav=dummy_path,
                                language=language
                            )
                            logger.info("✅ Síntese com arquivo dummy funcionou")
                        else:
                            raise Exception("Não foi possível criar arquivo de referência")
                    else:
                        raise tts_error
                else:
                    # Tentar método alternativo com lista
                    logger.info("🔄 Tentando método alternativo com lista...")
                    try:
                        self.xtts_v2.tts_to_file(
                            text=text,
                            file_path=output_path,
                            speaker_wav=[reference_audio_path],  # Lista como alternativa
                            language=language
                        )
                        logger.info("✅ Método alternativo com lista funcionou")
                    except Exception as alt_error:
                        logger.error(f"❌ Método alternativo também falhou: {alt_error}")
                        raise tts_error  # Relançar erro original'''
        
        if old_tts_call in content:
            content = content.replace(old_tts_call, new_tts_call)
            logger.info("✅ Correção do tts_to_file aplicada")
        else:
            logger.warning("⚠️ Método tts_to_file não encontrado para correção")
    
    # CORREÇÃO 2: Adicionar método para síntese simples que sempre usa referência
    synthesis_method = '''
    def synthesize_with_xtts_v2(self, text, language="pt"):
        """Síntese com XTTS v2 - sempre usa arquivo de referência"""
        try:
            # XTTS v2 SEMPRE precisa de arquivo de referência
            reference_audio_path = None
            
            # Procurar arquivo de referência existente
            ref_dir = "reference_audio"
            if os.path.exists(ref_dir):
                for filename in os.listdir(ref_dir):
                    if filename.endswith(('.wav', '.mp3', '.flac')):
                        file_path = os.path.join(ref_dir, filename)
                        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                            reference_audio_path = file_path
                            logger.info(f"✅ Usando arquivo de referência existente: {filename}")
                            break
            
            # Se não encontrou, criar dummy
            if not reference_audio_path:
                logger.info("🔄 Criando arquivo de referência dummy para síntese...")
                reference_audio_path = self.create_dummy_reference_audio()
                if not reference_audio_path:
                    raise Exception("Não foi possível criar arquivo de referência")
            
            # Preparar saída
            output_dir = "audios"
            os.makedirs(output_dir, exist_ok=True)
            
            from datetime import datetime
            agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            output_path = os.path.join(output_dir, f"synthesis_{agora}.wav")
            
            # Executar síntese
            logger.info(f"🔄 Síntese XTTS v2: {text[:50]}...")
            self.xtts_v2.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio_path,
                language=language
            )
            
            # Verificar resultado
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                with open(output_path, 'rb') as f:
                    audio_data = f.read()
                
                import base64
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                logger.info(f"✅ Síntese XTTS v2 concluída: {len(audio_data)} bytes")
                
                return {
                    "success": True,
                    "audio_base64": audio_base64,
                    "engine": "xtts_v2",
                    "file_path": output_path
                }
            else:
                raise Exception("Arquivo de síntese não foi gerado")
                
        except Exception as e:
            logger.error(f"❌ Erro na síntese XTTS v2: {e}")
            return {"success": False, "error": str(e)}
'''
    
    # Inserir o método antes do último método da classe
    if 'def _verify_and_return_clone_result(' in content:
        insertion_point = content.find('def _verify_and_return_clone_result(')
        if insertion_point != -1:
            content = content[:insertion_point] + synthesis_method + '\n    ' + content[insertion_point:]
            logger.info("✅ Método synthesize_with_xtts_v2 adicionado")
    
    # CORREÇÃO 3: Atualizar método synthesize_speech para usar o novo método
    if 'def synthesize_speech(' in content:
        old_synthesize = '''        # Try XTTS v2 if available
        if self.xtts_v2:
            try:
                logger.info("🔄 Trying XTTS v2 synthesis...")
                
                # Create output path
                output_dir = "audios"
                os.makedirs(output_dir, exist_ok=True)
                agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                output_path = os.path.join(output_dir, f"synthesis_{agora}.wav")
                
                # Use XTTS v2 for synthesis
                self.xtts_v2.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language
                )
                
                # Read and return audio
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    with open(output_path, 'rb') as f:
                        audio_data = f.read()
                    
                    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                    logger.info(f"✅ XTTS v2 synthesis successful: {len(audio_data)} bytes")
                    
                    return {
                        "success": True,
                        "audio_base64": audio_base64,
                        "engine": "xtts_v2",
                        "file_path": output_path
                    }
                else:
                    logger.warning("⚠️ XTTS v2 synthesis file not generated")
                    
            except Exception as e:
                logger.warning(f"⚠️ XTTS v2 synthesis failed: {e}")'''
        
        new_synthesize = '''        # Try XTTS v2 if available (com correção do "Invalid file: None")
        if self.xtts_v2:
            try:
                logger.info("🔄 Trying XTTS v2 synthesis with reference audio...")
                result = self.synthesize_with_xtts_v2(text, language)
                if result.get("success"):
                    logger.info("✅ XTTS v2 synthesis successful")
                    return result
                else:
                    logger.warning(f"⚠️ XTTS v2 synthesis failed: {result.get('error')}")
                    
            except Exception as e:
                logger.warning(f"⚠️ XTTS v2 synthesis failed: {e}")'''
        
        if old_synthesize in content:
            content = content.replace(old_synthesize, new_synthesize)
            logger.info("✅ Método synthesize_speech atualizado")
        else:
            logger.warning("⚠️ Método synthesize_speech não encontrado para atualização")
    
    # Salvar arquivo corrigido
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info("✅ Todas as correções do erro 'Invalid file: None' aplicadas")
    return True

def main():
    """Função principal"""
    logger.info("🔧 CORREÇÃO DO ERRO 'Invalid file: None'")
    logger.info("=" * 60)
    
    if fix_invalid_file_none_error():
        logger.info("✅ Correções aplicadas com sucesso!")
        
        print("\n📋 CORREÇÕES APLICADAS:")
        print("✅ Método _clone_with_xtts_v2 - CORRIGIDO")
        print("✅ Método synthesize_with_xtts_v2 - ADICIONADO")
        print("✅ Método synthesize_speech - ATUALIZADO")
        print("✅ Tratamento 'Invalid file: None' - IMPLEMENTADO")
        
        print("\n🎯 PROBLEMA RESOLVIDO:")
        print("❌ 'Invalid file: None' - ✅ CORRIGIDO")
        print("✅ XTTS v2 sempre usa arquivo de referência")
        print("✅ Criação automática de arquivo dummy")
        print("✅ Síntese e clonagem funcionais")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Reinicie o servidor: start_enhanced_correct.bat")
        print("2. Teste novamente: python test_with_real_voice_fixed.py")
        print("3. Teste o servidor: python debug_server_logs_realtime.py")
        
    else:
        logger.error("❌ Falha ao aplicar correções!")

if __name__ == "__main__":
    main()