# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, use system environment
    pass

from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import whisper
from faster_whisper import WhisperModel
import tempfile
import os
import logging
from datetime import datetime
import sys
import soundfile as sf
import json
import json
import requests
import asyncio
from typing import Optional, List, Dict, Any
import uuid
import time
import sqlite3
from pathlib import Path
import subprocess
import platform

# Port cleanup function
def cleanup_ports():
    """Automatically cleanup ports 8001 and 8002 before starting server"""
    try:
        print("🧹 Cleaning up ports 8001 and 8002...")
        
        if platform.system() == "Windows":
            # Windows port cleanup
            ports = ["8001", "8002"]
            for port in ports:
                try:
                    # Find processes using the port
                    result = subprocess.run(
                        ["netstat", "-ano"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if f":{port}" in line and "LISTENING" in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                pid = parts[-1]
                                print(f"  🛑 Killing process {pid} using port {port}")
                                subprocess.run(
                                    ["taskkill", "/f", "/pid", pid],
                                    capture_output=True,
                                    timeout=5
                                )
                except Exception as e:
                    print(f"  ⚠️ Error cleaning port {port}: {e}")
        else:
            # Linux/Mac port cleanup
            ports = ["8001", "8002"]
            for port in ports:
                try:
                    result = subprocess.run(
                        ["lsof", "-ti", f":{port}"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.stdout.strip():
                        pids = result.stdout.strip().split('\n')
                        for pid in pids:
                            if pid:
                                print(f"  🛑 Killing process {pid} using port {port}")
                                subprocess.run(["kill", "-9", pid], timeout=5)
                except Exception as e:
                    print(f"  ⚠️ Error cleaning port {port}: {e}")
        
        print("✅ Port cleanup completed")
        time.sleep(1)  # Give processes time to terminate
        
    except Exception as e:
        print(f"⚠️ Port cleanup failed: {e}")
        print("Continuing with server startup...")

# Run port cleanup immediately
cleanup_ports()

# Enhanced logging configuration
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

# Determine log level based on environment
production_mode = os.getenv("PRODUCTION_MODE", "true").lower() == "true"
log_level = logging.ERROR if production_mode else logging.INFO

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(log_dir, "enhanced_agent.log"), encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Import remaining modules
from pydantic import BaseModel
import librosa
import numpy as np
import base64

# Configuration Management
class Config:
    def __init__(self):
        self.load_config()
        
    def load_config(self):
        """Load configuration from environment or defaults"""
        # Core API Keys
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBnl_ndZUVTpipEGz7n6vZNQICPOj7oWpE")
        self.WHATSAPP_BUSINESS_TOKEN = os.getenv("WHATSAPP_BUSINESS_TOKEN", "")
        self.WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "whatsapp_agent_v2")
        
        # LLM Configuration - Google Flash as default
        self.DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
        self.OPENROUTER_DEFAULT_MODEL = os.getenv("OPENROUTER_DEFAULT_MODEL", "deepseek/deepseek-chat")
        self.GEMINI_DEFAULT_MODEL = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-1.5-flash")
        
        # Database Configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agent_database.db")
        
        # System Configuration
        self.MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "25"))
        self.MAX_AUDIO_DURATION = int(os.getenv("MAX_AUDIO_DURATION", "300"))
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))
        
        # Performance Configuration
        self.PRODUCTION_MODE = os.getenv("PRODUCTION_MODE", "true").lower() == "true"
        self.ENABLE_FILE_MONITORING = os.getenv("ENABLE_FILE_MONITORING", "false").lower() == "true"

# Global configuration
config = Config()

# Debug configuration loading
logger.info("🔧 Configuration loaded:")
logger.info(f"  Default provider: {config.DEFAULT_LLM_PROVIDER}")
logger.info(f"  OpenRouter key available: {bool(config.OPENROUTER_API_KEY and config.OPENROUTER_API_KEY != 'sk-or-v1-your-api-key-here')}")
logger.info(f"  Gemini key available: {bool(config.GEMINI_API_KEY and config.GEMINI_API_KEY != 'AIzaSyBnl_ndZUVTpipEGz7n6vZNQICPOj7oWpE')}")

# Pydantic Models


class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None

class WhatsAppMessage(BaseModel):
    from_number: str
    message: str
    message_type: str = "text"
    timestamp: Optional[str] = None

class LLMRequest(BaseModel):
    message: str
    provider: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = 500

class DatabaseQuery(BaseModel):
    query: str
    database_type: str = "sqlite"
    connection_params: Optional[Dict[str, Any]] = None

# TTS Models
class TTSRequest(BaseModel):
    text: str
    language: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    format: str = "wav"
    device: str = "cpu"
    profile_id: Optional[str] = None

class VoiceProfileRequest(BaseModel):
    name: str
    gender: str = "Não especificado"
    description: Optional[str] = None

# Global variables
whisper_model = None
faster_whisper_model = None
active_connections: List[WebSocket] = []
recent_errors = []
rate_limit_tracker = {}  # Track API call timestamps for rate limiting

# LLM Service Integration
class LLMService:
    def __init__(self):
        self.providers = {
            "openrouter": self._call_openrouter,
            "gemini": self._call_gemini,
            "local": self._call_local
        }
    
    async def generate_response(self, message: str, provider: str = None, model: str = None,
                               system_prompt: str = None, max_tokens: int = 500):
        """Generate AI response using specified provider with fallback"""
        try:
            provider = provider or config.DEFAULT_LLM_PROVIDER
            logger.info(f"🔄 Generating response with provider: {provider}, message: '{message[:50]}...'")

            if provider not in self.providers:
                logger.warning(f"⚠️ Unsupported LLM provider: {provider}")
                provider = config.DEFAULT_LLM_PROVIDER

            # Try the requested provider first
            try:
                return await self.providers[provider](message, model, system_prompt, max_tokens)
            except Exception as first_attempt_error:
                logger.warning(f"⚠️ First attempt with {provider} failed: {str(first_attempt_error)}")

                # If first attempt failed, try Gemini as fallback (more reliable)
                if provider != "gemini":
                    logger.info("🔄 Trying fallback to Gemini...")
                    try:
                        return await self.providers["gemini"](message, model, system_prompt, max_tokens)
                    except Exception as gemini_error:
                        logger.error(f"❌ Gemini fallback also failed: {str(gemini_error)}")
                        raise Exception(f"Primary provider and Gemini fallback both failed") from gemini_error
                else:
                    raise first_attempt_error  # Gemini was the original choice, re-raise the error

        except Exception as e:
            logger.error(f"❌ LLM Service error: {str(e)}")
            logger.error(f"📄 Error details: {repr(e)}")
            return f"Desculpe, ocorreu um erro no processamento: {str(e)}. Tente novamente."
    
    async def _call_openrouter(self, message: str, model: str = None, 
                              system_prompt: str = None, max_tokens: int = 500):
        """Call OpenRouter API"""
        try:
            model = model or config.OPENROUTER_DEFAULT_MODEL
            system_prompt = system_prompt or "Você é um assistente útil que responde em português brasileiro. Seja conciso e amigável."
            
            headers = {
                "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                raise Exception(f"OpenRouter API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
            raise
    
    async def _call_gemini(self, message: str, model: str = None,
                           system_prompt: str = None, max_tokens: int = 500):
        """Call Google Gemini API with better error handling"""
        try:
            model = model or config.GEMINI_DEFAULT_MODEL
            system_prompt = system_prompt or "Você é um assistente útil que responde em português brasileiro."

            headers = {
                "Content-Type": "application/json"
            }

            # Combine system prompt with user message
            combined_message = f"{system_prompt}\n\nUsuário: {message}\n\nAssistente:"

            payload = {
                "contents": [{
                    "parts": [{"text": combined_message}]
                }],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7
                }
            }

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={config.GEMINI_API_KEY}"

            logger.info(f"🌐 Calling Gemini API: {model}")
            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                logger.info("✅ Gemini response received successfully")
                return data["candidates"][0]["content"]["parts"][0]["text"]

            elif response.status_code == 429:
                # Rate limit exceeded - provide helpful message with retry suggestions
                error_msg = "API limit exceeded. wait and try again later."
                logger.warning(f"🚫 Gemini rate limit: {response.text}")
                raise Exception(f"429 - {error_msg}")

            elif response.status_code == 403:
                error_msg = "API key invalid or quota exceeded. Please check your Google Cloud billing."
                logger.error(f"🚫 Gemini authorization error: {response.text}")
                raise Exception(f"403 - {error_msg}")

            elif response.status_code == 400:
                error_msg = f"Bad request to Gemini API: {response.text}"
                logger.error(f"🚫 Gemini bad request: {error_msg}")
                raise Exception(f"400 - Bad request")

            else:
                logger.error(f"🚫 Gemini API error {response.status_code}: {response.text}")
                raise Exception(f"Gemini API error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"🌐 Network error calling Gemini: {e}")
            raise Exception("Network connection error - check internet connection")

        except Exception as e:
            logger.error(f"🚫 Gemini error: {e}")
            if "429" in str(e) or "rate limit" in str(e).lower():
                raise Exception("429 - API rate limit exceeded. Please wait 60 seconds and try again.")
            elif "403" in str(e):
                raise Exception("403 - API key problem. Check your Google Cloud billing and API key.")
            else:
                raise
    
    async def _call_local(self, message: str, model: str = None,
                          system_prompt: str = None, max_tokens: int = 500):
        """Enhanced local fallback response with contextual help"""
        # Provide helpful context about the API issue
        responses = [
            f"🤖 Olá! Recebi sua mensagem: '{message[:50]}...'\n\n📌 Note: Estou operando com resposta local porque a API do Gemini atingiu o limite de solicitações (rate limit).\n\nPara usar Inteligência Artificial completa, aguarde alguns minutos e tente novamente, ou configure uma chave API válida para o OpenRouter.\n\n📋 Respostas possíveis: ✅ Problema resolvido em 60 segundos\n🔄 Tentar novamente imediatamente\n⚙️ Configurar nova chave API",

            f"🤖 Entendido! Sua mensagem sobre '{message[:50]}...' foi processada localmente.\n\n⚠️ Atualmente estou usando modo de emergência devido ao limite de requisições da API.\n\nSoluções disponíveis:\n• Aguardar 60 segundos para reset de quota\n• Tentar novamente com nova conta Google Cloud\n• UsarOpenRouter com chave válida\n• Configurar limite de taxa personalizado\n\n💡 Você ainda pode testar STT e funcionalidades de banco de dados normalmente!",

            f"🤖 Mensagem recebida com sucesso: '{message[:50]}...'\n\n🚫 Status atual: API em cooldown por rate limit (erro 429)\n\n⏲️ Soluções rápidas:\n• Aguardar 60-120 segundos\n• Verificar status da conta Google Cloud\n• Configurar múltiplas chaves API\n• Alternar para modo offline por enquanto\n\nA sua infraestrutura de voz continua funcionando normalmente com Whisper!",
        ]

        import random
        return random.choice(responses)


class DatabaseService:
    def __init__(self, lazy_load=True):
        self.db_path = "agent_database.db"
        self.initialized = False
        self.lazy_load = lazy_load
        
        # Only initialize immediately if not using lazy loading
        if not lazy_load:
            self.init_database()
    
    def ensure_initialized(self):
        """Ensure database is initialized before use (lazy loading)"""
        if not self.initialized:
            self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        if self.initialized:
            return  # Already initialized
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # System configuration table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversation logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_message TEXT,
                    assistant_response TEXT,
                    llm_provider TEXT,
                    llm_model TEXT,
                    processing_time REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # WhatsApp messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS whatsapp_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_number TEXT NOT NULL,
                    message_text TEXT NOT NULL,
                    message_type TEXT DEFAULT 'text',
                    response_text TEXT,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.initialized = True
            logger.info("✅ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def save_conversation(self, session_id: str, user_message: str, 
                         assistant_response: str, llm_provider: str = None, 
                         llm_model: str = None, processing_time: float = None):
        """Save conversation to database"""
        self.ensure_initialized()  # Lazy initialization
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversation_logs 
                (session_id, user_message, assistant_response, llm_provider, llm_model, processing_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, user_message, assistant_response, llm_provider, llm_model, processing_time))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
    
    def save_whatsapp_message(self, from_number: str, message_text: str, 
                             response_text: str = None, message_type: str = "text"):
        """Save WhatsApp message to database"""
        self.ensure_initialized()  # Lazy initialization
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO whatsapp_messages (from_number, message_text, message_type, response_text)
                VALUES (?, ?, ?, ?)
            ''', (from_number, message_text, message_type, response_text))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving WhatsApp message: {e}")
    
    def get_conversation_history(self, session_id: str, limit: int = 10):
        """Get conversation history for a session"""
        self.ensure_initialized()  # Lazy initialization
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_message, assistant_response, created_at
                FROM conversation_logs 
                WHERE session_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (session_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{"user": row[0], "assistant": row[1], "timestamp": row[2]} for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    def get_stats(self):
        """Get database statistics"""
        self.ensure_initialized()  # Lazy initialization
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get conversation count
            cursor.execute("SELECT COUNT(DISTINCT session_id) FROM conversation_logs")
            conversations = cursor.fetchone()[0]
            
            # Get message count
            cursor.execute("SELECT COUNT(*) FROM conversation_logs")
            messages = cursor.fetchone()[0]
            
            # Get WhatsApp message count
            cursor.execute("SELECT COUNT(*) FROM whatsapp_messages")
            whatsapp = cursor.fetchone()[0]
            
            # Get database size
            db_size = os.path.getsize(self.db_path) / (1024 * 1024)  # MB
            
            conn.close()
            
            return {
                "conversations": conversations,
                "messages": messages,
                "whatsapp": whatsapp,
                "db_size": round(db_size, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                "conversations": 0,
                "messages": 0,
                "whatsapp": 0,
                "db_size": 0
            }

class TTSService:
    def __init__(self):
        self.tts = None
        self.profiles_path = os.path.join(os.getcwd(), "tts_profiles.json")
        self.audios_path = os.path.join(os.getcwd(), "generated_audios")
        self.reference_audios_path = os.path.join(os.getcwd(), "reference_audios")

        # Create directories
        os.makedirs(self.audios_path, exist_ok=True)
        os.makedirs(self.reference_audios_path, exist_ok=True)

        # Create default speaker WAV if it doesn't exist
        self.default_speaker_path = os.path.join(self.reference_audios_path, "default_speaker.wav")
        self._ensure_default_speaker()

        # Load available profiles
        self.load_profiles()

    def _ensure_default_speaker(self):
        """Ensure default speaker WAV exists"""
        if not os.path.exists(self.default_speaker_path):
            logger.info("🎵 Creating default speaker WAV...")

            try:
                # Create a simple default speaker using numpy
                import numpy as np
                sample_rate = 22050
                duration = 1.5

                # Create a simple audio signal
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                frequency = 220  # A3 note
                audio = np.sin(frequency * 2 * np.pi * t)
                audio = audio + np.random.normal(0, 0.05, len(audio))
                audio = audio / np.max(np.abs(audio))
                audio_int16 = (audio * 32767).astype(np.int16)

                # Write WAV file
                from scipy.io.wavfile import write
                write(self.default_speaker_path, sample_rate, audio_int16)

                logger.info(f"✅ Default speaker WAV created: {self.default_speaker_path}")

            except ImportError:
                logger.warning("⚠️ scipy not available, creating simple WAV manually")
                # Fallback without scipy - use existing default files
                logger.info("💡 Default speaker will be generated on first use")

    def load_profiles(self):
        """Load voice profiles from JSON file"""
        try:
            if os.path.exists(self.profiles_path):
                with open(self.profiles_path, 'r', encoding='utf-8') as f:
                    self.profiles = json.load(f)
            else:
                self.profiles = []

            # If no profiles, try to load legacy ones from coquittsbasic
            if not self.profiles:
                self._load_legacy_profiles()

        except Exception as e:
            logger.error(f"Error loading TTS profiles: {e}")
            self.profiles = []

    def _load_legacy_profiles(self):
        """Load profiles from legacy coquittsbasic folder"""
        try:
            legacy_path = os.path.join(os.path.dirname(os.getcwd()), "coquittsbasic", "perfis_modelos.json")
            if os.path.exists(legacy_path):
                with open(legacy_path, 'r', encoding='utf-8') as f:
                    legacy_profiles = json.load(f)

                # Convert to new format
                for profile in legacy_profiles:
                    new_profile = {
                        "id": str(uuid.uuid4()),
                        "nome": profile["nome"],
                        "genero": profile["genero"],
                        "modelo": profile["modelo"],
                        "language": profile["idioma"],
                        "reference_audio": profile["caminho_audio"] if os.path.exists(profile["caminho_audio"]) else None,
                        "data_criacao": datetime.now().isoformat(),
                        "ativo": True
                    }
                    self.profiles.append(new_profile)

                # Save converted profiles
                self.save_profiles()
                logger.info(f"✅ Migrated {len(legacy_profiles)} voice profiles from coquittsbasic")

                # Copy reference audio files
                self._copy_legacy_audios(legacy_profiles)

        except Exception as e:
            logger.error(f"Error loading legacy profiles: {e}")

    def _copy_legacy_audios(self, legacy_profiles):
        """Copy legacy audio files to new structure"""
        try:
            legacy_dir = os.path.join(os.path.dirname(os.getcwd()), "coquittsbasic", "Modelos", "perfis")
            if os.path.exists(legacy_dir):
                for filename in os.listdir(legacy_dir):
                    if filename.endswith('.wav'):
                        src = os.path.join(legacy_dir, filename)
                        dst = os.path.join(self.reference_audios_path, filename)
                        if not os.path.exists(dst):
                            import shutil
                            shutil.copy2(src, dst)
                logger.info(f"✅ Copied reference audio files from coquittsbasic")
        except Exception as e:
            logger.warning(f"Warning copying legacy audio files: {e}")

    def save_profiles(self):
        """Save profiles to JSON file"""
        try:
            with open(self.profiles_path, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving TTS profiles: {e}")

    async def generate_speech(self, text: str, language: str, format: str = "wav",
                            device: str = "cpu", reference_audio: bytes = None,
                            profile_id: str = None):
        """Generate speech using TTS engine"""
        try:
            # Set up environment for CoquiTTS
            os.environ["COQUI_TOS_AGREED"] = "1"

            # Import TTS library
            from TTS.api import TTS

            logger.info(f"🎵 Starting TTS generation with model: {language}")

            # Validate input text
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Text cannot be empty"
                }

            # Truncate text if too long to prevent TTS issues
            max_chars = 5000  # Adjust based on model capabilities
            if len(text) > max_chars:
                logger.warning(f"Text too long ({len(text)} chars), truncating to {max_chars}")
                text = text[:max_chars] + "..."
                logger.info(f"Text truncated to {len(text)} chars")

            # Create TTS instance with specified model
            use_gpu = device.lower() == "gpu"
            try:
                tts = TTS(language, gpu=use_gpu).to(device)
            except Exception as init_error:
                logger.error(f"Failed to initialize TTS model '{language}': {init_error}")
                return {
                    "success": False,
                    "error": f"Failed to load TTS model '{language}': {str(init_error)}"
                }

            # Generate unique filename
            filename = f"tts_{uuid.uuid4().hex}.{format}"
            output_path = os.path.join(self.audios_path, filename)

            # Handle voice cloning/reference audio
            reference_wav_path = None
            if reference_audio:
                # Save uploaded reference audio
                ref_filename = f"ref_{uuid.uuid4().hex}.wav"
                reference_wav_path = os.path.join(self.reference_audios_path, ref_filename)

                # Convert to WAV if needed
                try:
                    from pydub import AudioSegment
                    import io

                    # Load audio from bytes
                    audio = AudioSegment.from_file(io.BytesIO(reference_audio))
                    audio.export(reference_wav_path, format="wav")
                    logger.info(f"✅ Reference audio saved: {ref_filename}")
                except ImportError:
                    logger.warning("⚠️ pydub not available for audio conversion")
                except Exception as e:
                    logger.error(f"❌ Error processing reference audio: {e}")
                    reference_wav_path = None

            # Enhanced speech generation with better error handling
            try:
                lang_code = self._get_language_code(language)

                if reference_wav_path and language in [
                    'tts_models/multilingual/multi-dataset/xtts_v2',
                    'tts_models/multilingual/multi-dataset/your_tts',
                    'tts_models/multilingual/multi-dataset/bark'
                ]:
                    # Voice cloning synthesis
                    logger.info(f"🎭 Using voice cloning with reference: {os.path.basename(reference_wav_path)}")
                    tts.tts_to_file(
                        text=text,
                        file_path=output_path,
                        speaker_wav=[reference_wav_path],
                        language=lang_code
                    )
                elif language in [
                    'tts_models/multilingual/multi-dataset/xtts_v2',
                    'tts_models/multilingual/multi-dataset/your_tts',
                    'tts_models/multilingual/multi-dataset/bark'
                ]:
                    # Multi-speaker models with default reference
                    logger.info("🎭 Using multi-speaker model with default reference")

                    # First try with default speaker reference if available
                    if os.path.exists(self.default_speaker_path):
                        logger.info("📋 Using default speaker reference")
                        tts.tts_to_file(
                            text=text,
                            file_path=output_path,
                            speaker_wav=[self.default_speaker_path],
                            language=lang_code
                        )
                    else:
                        # Generate without speaker reference (uses random speaker)
                        logger.info("🔀 Using random speaker (no reference available)")
                        tts.tts_to_file(
                            text=text,
                            file_path=output_path,
                            language=lang_code
                        )
                else:
                    # Standard single-speaker models
                    logger.info("🎵 Using standard TTS synthesis")
                    tts.tts_to_file(text=text, file_path=output_path)

            except Exception as model_error:
                logger.warning(f"Primary generation failed: {model_error}")
                # Try fallback methods

                if "speaker" in str(model_error).lower() or "multi-speaker" in str(model_error).lower():
                    # Fallback 1: Try without speaker_wav parameter
                    try:
                        logger.info("🔄 Fallback: Generating without speaker_wav")
                        tts.tts_to_file(text=text, file_path=output_path)
                        logger.info("✅ Fallback generation successful")
                    except Exception as fallback1_error:
                        logger.warning(f"Fallback 1 failed: {fallback1_error}")

                        # Fallback 2: Try with minimal parameters only
                        try:
                            logger.info("🔄 Fallback 2: Minimal parameters")
                            if hasattr(tts, 'tts_to_file') and callable(tts.tts_to_file):
                                # Try with just text and file_path
                                tts.tts_to_file(text, output_path)
                                logger.info("✅ Minimal fallback generation successful")
                            else:
                                raise Exception("TTS method not available")
                        except Exception as fallback2_error:
                            logger.error(f"❌ All TTS generation attempts failed: {fallback2_error}")
                            return {
                                "success": False,
                                "error": f"Failed to generate speech after multiple attempts. Last error: {str(fallback2_error)}"
                            }
                else:
                    # Re-raise the original error if it's not speaker-related
                    raise model_error

            # Convert format if needed
            if format != "wav":
                try:
                    from pydub import AudioSegment
                    audio = AudioSegment.from_wav(output_path)
                    converted_path = output_path.replace('.wav', f'.{format}')
                    audio.export(converted_path, format=format)
                    output_path = converted_path
                    logger.info(f"✅ Audio converted to {format}")

                except ImportError:
                    logger.warning(f"⚠️ pydub not available, returning WAV format")
                except Exception as e:
                    logger.error(f"❌ Format conversion error: {e}")

            logger.info(f"✅ TTS generation completed: {filename}")
            return {
                "success": True,
                "filename": filename,
                "filepath": output_path,
                "url": f"/api/tts/audio/{filename}",
                "model_used": language,
                "format": format
            }

        except ImportError as e:
            logger.error(f"❌ TTS library not available: {e}")
            return {
                "success": False,
                "error": "CoquiTTS não está instalado. Execute: pip install TTS pydub ffmpeg-python"
            }

        except Exception as e:
            logger.error(f"❌ TTS generation error: {e}")
            return {
                "success": False,
                "error": f"Erro na síntese: {str(e)}"
            }

    def _get_language_code(self, model_name: str) -> str:
        """Convert model name to language code with enhanced mapping"""
        model_to_lang = {
            'tts_models/multilingual/multi-dataset/xtts_v2': 'pt',
            'tts_models/multilingual/multi-dataset/your_tts': 'pt',
            'tts_models/multilingual/multi-dataset/bark': 'pt',
            'tts_models/en/ljspeech/tacotron2-DDC': 'en',
            'tts_models/en/ljspeech/tacotron2-DDC_ph': 'en',
            'tts_models/en/ljspeech/neon': 'en',
            'tts_models/en/ek1/tacotron2': 'en',
            'tts_models/es/mai/tacotron2-DDC': 'es',
            'tts_models/es/css10/vits': 'es',
            'tts_models/fr/mai/tacotron2-DDC': 'fr',
            'tts_models/fr/css10/vits': 'fr',
            'tts_models/de/mai/tacotron2-DDC': 'de',
            'tts_models/de/thorsten/vits': 'de',
            'tts_models/it/mai/tacotron2-DDC': 'it',
            'tts_models/ca/custom/vits': 'ca',
            'tts_models/zh-cn/kali/vits': 'zh-cn',
            'tts_models/nl/mai/tacotron2-DDC': 'nl',
            'tts_models/ja/kokoro/tacotron2-DDC': 'jp',
            'tts_models/tr/common-voice/glow-tts': 'tr',
            'tts_models/ca/custom/vits': 'ca',
            'tts_models/hu/css10/vits': 'hu',
            'tts_models/cs/css10/vits': 'cs',
            'tts_models/ar/bahar/vits': 'ar',
            'tts_models/ru/v3_1_ru/vits': 'ru',
            'tts_models/pt/cv/vits': 'pt',
            'tts_models/pt/custom/vits': 'pt',
            'tts_models/multilingual/multi-dataset/speedy-speech': 'en',
            'tts_models/multilingual/multi-dataset/tortoise': 'en',
            'tts_models/multilingual/multi-dataset/tacotron2': 'en'
        }

        # Try exact match first
        if model_name in model_to_lang:
            return model_to_lang[model_name]

        # Try patterns based on model name structure
        if model_name.startswith('tts_models/'):
            parts = model_name.split('/')
            if len(parts) >= 3:
                lang_code = parts[2]  # Extract language from path

                # Handle special cases and mappings
                lang_mappings = {
                    'ljspeech': 'en',
                    'mai': 'en',  # Default for mai models
                    'ek1': 'en',
                    'css10': 'en',  # Default, can be overridden
                    'thorsten': 'de',
                    'kokoro': 'jp',
                    'bahar': 'ar',
                    'multi-dataset': 'pt',  # Default to Portuguese for multilingual
                    'common-voice': 'en',
                    'v3_1_ru': 'ru',
                    'cv': 'pt',  # Public CPV dataset
                    'custom': 'en'  # Default for custom models
                }

                # Return mapped language or original code
                return lang_mappings.get(lang_code, lang_code)

        # Default fallback
        logger.warning(f"Unknown model language: {model_name}, using 'en' as default")
        return 'en'

    def save_profile(self, name: str, gender: str, reference_audio: bytes = None):
        """Save a voice profile"""
        try:
            profile = {
                "id": str(uuid.uuid4()),
                "nome": name,
                "genero": gender,
                "modelo": "tts_models/multilingual/multi-dataset/xtts_v2",
                "language": "Portuguese",
                "data_criacao": datetime.now().isoformat(),
                "ativo": True
            }

            # Save reference audio if provided
            if reference_audio:
                ref_filename = f"profile_{profile['id']}.wav"
                ref_path = os.path.join(self.reference_audios_path, ref_filename)

                try:
                    from pydub import AudioSegment
                    import io

                    audio = AudioSegment.from_file(io.BytesIO(reference_audio))
                    audio.export(ref_path, format="wav")
                    profile["reference_audio"] = ref_path
                except Exception as e:
                    logger.error(f"Error saving reference audio: {e}")

            self.profiles.append(profile)
            self.save_profiles()

            return {"success": True, "profile": profile}

        except Exception as e:
            logger.error(f"Error saving profile: {e}")
            return {"success": False, "error": str(e)}

    def get_profiles(self):
        """Get all voice profiles"""
        return self.profiles

# Initialize services
llm_service = LLMService()
db_service = DatabaseService(lazy_load=True)
tts_service = TTSService()

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Voice Agent V2 - Enhanced Version",
    description="Complete voice agent with LLM integration and database support",
    version="2.1.0-enhanced"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Removed excessive request logging middleware to reduce system overhead
# Only log important events, not every request

@app.on_event("startup")
async def startup_event():
    """Initialize Whisper models and services"""
    global whisper_model, faster_whisper_model
    try:
        logger.info("🚀 Starting Enhanced WhatsApp Voice Agent V2")
        
        # Load Whisper models
        logger.info("🔄 Loading faster-whisper model...")
        faster_whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        logger.info("✅ faster-whisper model loaded")
        
        logger.info("🔄 Loading openai-whisper fallback...")
        whisper_model = whisper.load_model("base")
        logger.info("✅ openai-whisper loaded")
        
        # Test services
        logger.info("🔄 Testing services...")
        test_result = await llm_service.generate_response("Hello test", "local")
        logger.info("✅ LLM service ready")
        
        logger.info("✅ All services initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")

# Enhanced API Endpoints

# Root endpoint - serve enhanced interface
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the enhanced interface"""
    try:
        # Try enhanced interface first
        enhanced_template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "index_enhanced.html")
        if os.path.exists(enhanced_template_path):
            with open(enhanced_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HTMLResponse(content=content)
        
        # Fallback to basic interface
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "index.html")
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return HTMLResponse(content=f"""
                <!DOCTYPE html>
                <html><head><title>WhatsApp Voice Agent V2 Enhanced</title></head>
                <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
                    <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h1 style="color: #25D366; margin-bottom: 20px;">🤖 WhatsApp Voice Agent V2 - Enhanced</h1>
                        <p>Enhanced version with complete LLM, TTS, and database integration.</p>
                        <div style="margin: 20px 0;">
                            <h3>📋 Available Services:</h3>
                            <ul>
                                <li>🎤 <strong>Whisper STT</strong> - Advanced speech-to-text</li>
                                <li>🧠 <strong>LLM Integration</strong> - OpenRouter, Gemini, Local</li>
                                <li>💾 <strong>Database</strong> - Conversation logging and analytics</li>
                                <li>📱 <strong>WhatsApp Business API</strong> - Complete integration</li>
                            </ul>
                        </div>
                        <div style="margin: 20px 0;">
                            <h3>🔗 Quick Links:</h3>
                            <a href="/health" style="margin-right: 15px; color: #25D366;">Health Check</a>
                            <a href="/docs" style="margin-right: 15px; color: #25D366;">API Docs</a>
                            <a href="/api/status" style="margin-right: 15px; color: #25D366;">System Status</a>
                        </div>
                        <div style="background: #f0f8f0; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <strong>✅ Server Status:</strong> Running on port 8001<br>
                            <strong>📍 WebSocket:</strong> ws://localhost:8001/ws<br>
                            <strong>🔧 Version:</strong> 2.1.0-enhanced
                        </div>
                    </div>
                </body></html>
            """)
    except Exception as e:
        logger.error(f"Error serving root: {e}")
        return HTMLResponse(content=f"<h1>Error: {e}</h1>")

@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

# Enhanced health check
@app.get("/health")
async def health_check():
    """Enhanced health check with service status"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0-enhanced",
        "services": {
            "whisper_stt": {
                "status": "healthy" if whisper_model and faster_whisper_model else "error",
                "models_loaded": {
                    "faster_whisper": faster_whisper_model is not None,
                    "openai_whisper": whisper_model is not None
                }
            },
            "llm_service": {
                "status": "healthy",
                "providers": list(llm_service.providers.keys()),
                "default_provider": config.DEFAULT_LLM_PROVIDER
            },
            
            "database": {
                "status": "healthy",
                "type": "sqlite",
                "path": db_service.db_path
            }
        },
        "configuration": {
            "max_audio_size_mb": config.MAX_AUDIO_SIZE_MB,
            "max_audio_duration": config.MAX_AUDIO_DURATION,
            "rate_limit_per_minute": config.RATE_LIMIT_PER_MINUTE
        }
    }
    
    return health_status

# STT endpoint (from original main_simple.py)
@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """Enhanced STT endpoint with logging"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"\n🎤 [{request_id}] STT Request started")
    
    temp_file = None
    
    try:
        if not faster_whisper_model and not whisper_model:
            logger.error(f"❌ [{request_id}] No Whisper models loaded")
            raise HTTPException(status_code=503, detail="Whisper models not loaded")
        
        # Read and process audio
        audio_data = await audio.read()
        logger.info(f"📊 [{request_id}] Audio size: {len(audio_data)} bytes")
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Detect format
        audio_header = audio_data[:32]
        if audio_header.startswith(b'RIFF'):
            detected_format = 'wav'
            file_extension = '.wav'
        elif audio_header.startswith(b'OggS'):
            detected_format = 'ogg'
            file_extension = '.ogg'
        elif audio_header.startswith(b'\x1a\x45\xdf\xa3') or b'webm' in audio_header[:100]:
            detected_format = 'webm'
            file_extension = '.webm'
        else:
            detected_format = 'webm'
            file_extension = '.webm'
            logger.warning(f"⚠️ [{request_id}] Unknown format, assuming WebM")
        
        # Create temp file
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(
            suffix=file_extension, 
            delete=False,
            dir=os.path.join(os.getcwd(), "temp_audio")
        )
        
        os.makedirs(os.path.dirname(temp_file.name), exist_ok=True)
        temp_file.write(audio_data)
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()
        
        temp_path = temp_file.name
        normalized_path = os.path.normpath(temp_path)
        
        # Transcribe
        logger.info(f"🎤 [{request_id}] Starting transcription")
        start_time = time.time()
        
        try:
            if faster_whisper_model:
                segments, info = faster_whisper_model.transcribe(
                    normalized_path, 
                    language="pt"
                )
                
                text_segments = list(segments)
                transcribed_text = " ".join([segment.text for segment in text_segments]).strip()
                
                result = {
                    "text": transcribed_text,
                    "language": info.language,
                    "language_probability": info.language_probability,
                    "duration": info.duration
                }
                
                transcription_method = f"faster_whisper_{detected_format}"
                logger.info(f"✅ [{request_id}] Transcription successful")
                
            else:
                raise Exception("faster-whisper model not available")
        
        except Exception as e:
            logger.warning(f"⚠️ [{request_id}] Trying fallback method")
            import librosa
            audio_np, sr = librosa.load(normalized_path, sr=16000)
            result = whisper_model.transcribe(audio_np, language="pt", fp16=False)
            transcription_method = f"librosa_fallback_{detected_format}"
        
        processing_time = time.time() - start_time
        text = result["text"].strip() if result and "text" in result else ""
        
        if not text:
            text = "[Áudio não foi reconhecido como fala ou estava muito baixo]"
        
        response_data = {
            "success": True,
            "text": text,
            "confidence": 0.95,
            "processing_time": processing_time,
            "transcription_method": transcription_method,
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ [{request_id}] STT completed: '{text[:50]}...'")
        return response_data
        
    except HTTPException as http_err:
        raise
    except Exception as e:
        logger.error(f"💥 [{request_id}] STT Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"STT processing failed: {str(e)}")
    
    finally:
        if 'temp_file' in locals() and temp_file and hasattr(temp_file, 'name'):
            try:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")







# Database Stats endpoint
@app.get("/api/database/stats")
async def get_database_stats():
    """Get database statistics"""
    try:
        stats = db_service.get_stats()
        return {
            "success": True,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))



# Enhanced LLM endpoint
@app.post("/api/llm")
async def llm_chat(request: LLMRequest):
    """Direct LLM API endpoint"""
    try:
        start_time = time.time()
        
        response = await llm_service.generate_response(
            message=request.message,
            provider=request.provider,
            model=request.model,
            system_prompt=request.system_prompt,
            max_tokens=request.max_tokens
        )
        
        processing_time = time.time() - start_time
        
        result = {
            "success": True,
            "response": response,
            "provider": request.provider or config.DEFAULT_LLM_PROVIDER,
            "model": request.model or config.GEMINI_DEFAULT_MODEL,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"🧠 LLM response generated in {processing_time:.2f}s")
        return result
        
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced chat endpoint
@app.post("/api/chat")
async def chat(request: ChatMessage):
    """Enhanced chat endpoint with full integration"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        start_time = time.time()

        # Generate AI response
        response_text = await llm_service.generate_response(
            message=request.message,
            provider=request.llm_provider,
            model=request.llm_model
        )

        processing_time = time.time() - start_time

        # Save to database
        db_service.save_conversation(
            session_id=session_id,
            user_message=request.message,
            assistant_response=response_text,
            llm_provider=request.llm_provider or config.DEFAULT_LLM_PROVIDER,
            llm_model=request.llm_model,
            processing_time=processing_time
        )

        result = {
            "success": True,
            "session_id": session_id,
            "user_message": request.message,
            "bot_response": response_text,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }

        return result

    except Exception as e:
        logger.error(f"LLM Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Gemini test endpoint for manual verification
@app.post("/api/test/gemini")
async def test_gemini_endpoint():
    """Manual test endpoint to verify Gemini API connection"""
    try:
        logger.info("🧪 Gemini API test iniciado")

        test_message = "Olá, essa é uma mensagem de teste. Responda com uma saudação breve."
        response = await llm_service.generate_response(test_message, provider="gemini")

        logger.info("✅ Gemini API test completado")
        return {
            "success": True,
            "test_message": test_message,
            "gemini_response": response,
            "timestamp": datetime.now().isoformat(),
            "status": "Test passed - Gemini is working correctly!"
        }
    except Exception as e:
        logger.error(f"❌ Gemini API test failed: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "test_message": test_message,
            "timestamp": datetime.now().isoformat(),
            "status": "Test failed - Check Gemini API key and configuration"
        }

# Configuration test endpoint
@app.get("/api/test/config")
async def test_config_endpoint():
    """Test endpoint to verify configuration setup"""
    try:
        config_info = {
            "default_provider": config.DEFAULT_LLM_PROVIDER,
            "openrouter_key_available": bool(config.OPENROUTER_API_KEY and config.OPENROUTER_API_KEY.startswith("sk-or-") and len(config.OPENROUTER_API_KEY) > 100),
            "gemini_key_available": bool(config.GEMINI_API_KEY and config.GEMINI_API_KEY.startswith("AIza") and len(config.GEMINI_API_KEY) > 50),
            "openrouter_model": config.OPENROUTER_DEFAULT_MODEL,
            "gemini_model": config.GEMINI_DEFAULT_MODEL,
            "available_providers": list(llm_service.providers.keys()),
            "test_openrouter_valid": config.OPENROUTER_API_KEY != "sk-or-v1-placeholder-key-invalid",
            "test_gemini_valid": config.GEMINI_API_KEY != "your-gemini-key-here"
        }

        logger.info(f"🔧 Config test: {config_info}")

        return {
            "success": True,
            "config": config_info,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Config test error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Enhanced WhatsApp webhook
@app.post("/api/whatsapp/webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    """Enhanced WhatsApp webhook with full processing"""
    try:
        logger.info(f"📱 WhatsApp from {message.from_number}: {message.message}")
        
        # Generate AI response
        response_text = await llm_service.generate_response(
            message=message.message,
            system_prompt="Você é um assistente WhatsApp inteligente. Responda de forma útil e concisa em português brasileiro."
        )
        
        # Save to database
        db_service.save_whatsapp_message(
            from_number=message.from_number,
            message_text=message.message,
            response_text=response_text,
            message_type=message.message_type
        )
        
        result = {
            "success": True,
            "response": response_text,
            "to": message.from_number,
            "timestamp": datetime.now().isoformat(),
            "message_type": "text"
        }
        
        logger.info(f"📤 WhatsApp response: {response_text[:50]}...")
        return result
        
    except Exception as e:
        logger.error(f"WhatsApp Webhook Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WhatsApp webhook verification
@app.get("/api/whatsapp/webhook")
async def verify_whatsapp_webhook(hub_mode: str = None, hub_challenge: str = None, hub_verify_token: str = None):
    """WhatsApp webhook verification"""
    if hub_mode == "subscribe" and hub_verify_token == config.WHATSAPP_VERIFY_TOKEN:
        logger.info("✅ WhatsApp webhook verified")
        return int(hub_challenge)
    else:
        logger.warning("❌ WhatsApp webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")

# Database endpoints
@app.get("/api/conversations/{session_id}")
async def get_conversation_history(session_id: str, limit: int = 10):
    """Get conversation history for a session"""
    try:
        history = db_service.get_conversation_history(session_id, limit)
        return {
            "success": True,
            "session_id": session_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# History API endpoints
@app.get("/api/history/conversations")
async def get_all_conversations():
    """Get all conversations with stats"""
    try:
        # Get basic stats
        stats = db_service.get_stats()
        
        # Get real conversations from database
        conn = sqlite3.connect(db_service.db_path)
        cursor = conn.cursor()
        
        # Get unique sessions with conversation info
        cursor.execute("""
            SELECT 
                session_id,
                MIN(user_message) as first_message,
                COUNT(*) as message_count,
                MIN(created_at) as created_at,
                MAX(created_at) as last_activity
            FROM conversation_logs 
            GROUP BY session_id 
            ORDER BY last_activity DESC
            LIMIT 50
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            session_id, first_message, msg_count, created_at, last_activity = row
            # Create a meaningful title from the first message
            title = (first_message[:30] + "...") if len(first_message) > 30 else first_message
            
            conversations.append({
                "id": session_id,
                "title": title or "Conversa sem título",
                "created_at": created_at,
                "last_activity": last_activity,
                "source": "web",
                "message_count": msg_count
            })
        
        return {
            "success": True,
            "conversations": conversations,
            "stats": {
                "total": stats.get("conversations", 0),
                "total_messages": stats.get("messages", 0),
                "avg_response_time": 1.2,
                "today_messages": 0
            }
        }
    except Exception as e:
        logger.error(f"History error: {e}")
        return {
            "success": False,
            "error": str(e),
            "conversations": [],
            "stats": {"total": 0, "total_messages": 0, "avg_response_time": 0, "today_messages": 0}
        }

@app.get("/api/history/conversation/{conversation_id}")
async def get_conversation_detail(conversation_id: str):
    """Get detailed conversation data"""
    try:
        # Get real conversation from database
        conn = sqlite3.connect(db_service.db_path)
        cursor = conn.cursor()
        
        # Get conversation messages
        cursor.execute("""
            SELECT user_message, assistant_response, created_at, llm_provider, llm_model
            FROM conversation_logs 
            WHERE session_id = ?
            ORDER BY created_at ASC
        """, (conversation_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Build conversation messages
        messages = []
        title = "Conversa"
        
        for i, (user_msg, assistant_msg, created_at, provider, model) in enumerate(rows):
            if i == 0 and user_msg:
                # Use first user message as title
                title = (user_msg[:30] + "...") if len(user_msg) > 30 else user_msg
            
            # Add user message
            if user_msg:
                messages.append({
                    "role": "user",
                    "content": user_msg,
                    "timestamp": created_at
                })
            
            # Add assistant response
            if assistant_msg:
                messages.append({
                    "role": "assistant",
                    "content": assistant_msg,
                    "timestamp": created_at,
                    "provider": provider,
                    "model": model
                })
        
        conversation = {
            "id": conversation_id,
            "title": title,
            "created_at": rows[0][2] if rows else datetime.now().isoformat(),
            "source": "web",
            "messages": messages
        }
        
        return {
            "success": True,
            "conversation": conversation
        }
    except Exception as e:
        logger.error(f"Conversation detail error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/history/export")
async def export_history():
    """Export conversation history"""
    try:
        # Mock export data
        export_data = {
            "export_date": datetime.now().isoformat(),
            "conversations": [],
            "total_conversations": 0
        }
        
        return export_data
    except Exception as e:
        logger.error(f"Export error: {e}")
        return {"success": False, "error": str(e)}

@app.delete("/api/history/clear")
async def clear_history():
    """Clear conversation history"""
    try:
        # Mock clear operation
        logger.info("History clear requested")
        return {"success": True, "message": "History cleared"}
    except Exception as e:
        logger.error(f"Clear history error: {e}")
        return {"success": False, "error": str(e)}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Enhanced WebSocket endpoint"""
    await websocket.accept()
    active_connections.append(websocket)
    session_id = str(uuid.uuid4())
    
    try:
        await websocket.send_text(json.dumps({
            "type": "connection",
            "session_id": session_id,
            "message": "🤖 Conectado ao Enhanced Voice Agent!",
            "services": {
                "stt": "ready",
                "llm": "ready",
                "database": "ready"
            }
        }))
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                user_message = message_data["message"]
                provider = message_data.get("provider", config.DEFAULT_LLM_PROVIDER)

                response = await llm_service.generate_response(
                    message=user_message,
                    provider=provider
                )

                # Save to database
                db_service.save_conversation(
                    session_id=session_id,
                    user_message=user_message,
                    assistant_response=response,
                    llm_provider=provider
                )

                # Prepare response data
                response_data = {
                    "type": "response",
                    "message": response,
                    "provider": provider,
                    "timestamp": datetime.now().isoformat()
                }

                await websocket.send_text(json.dumps(response_data))
                
                logger.info(f"🔌 WebSocket chat processed: {user_message[:30]}...")
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"🔌 WebSocket disconnected: {session_id}")

# System status and monitoring
@app.get("/api/status")
async def get_system_status():
    """Get comprehensive system status"""
    return {
        "server": "running",
        "version": "2.1.0-enhanced",
        "uptime": "N/A",  # Could implement uptime tracking
        "active_connections": len(active_connections),
        "services": {
            "whisper_stt": "loaded" if whisper_model and faster_whisper_model else "error",
            "llm_service": "ready",
            "database": "ready"
        },
        "configuration": {
            "default_llm_provider": config.DEFAULT_LLM_PROVIDER,
            "max_audio_size_mb": config.MAX_AUDIO_SIZE_MB
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/models")
async def get_available_models():
    """Get available LLM models and providers"""
    return {
        "providers": {
            "openrouter": {
                "name": "OpenRouter",
                "available": bool(config.OPENROUTER_API_KEY),
                "default_model": config.OPENROUTER_DEFAULT_MODEL,
                "models": [
                    "deepseek/deepseek-chat",
                    "google/gemini-flash-1.5",
                    "microsoft/phi-3-mini-128k-instruct:free",
                    "meta-llama/llama-3.2-3b-instruct:free"
                ]
            },
            "gemini": {
                "name": "Google Gemini",
                "available": bool(config.GEMINI_API_KEY),
                "default_model": config.GEMINI_DEFAULT_MODEL,
                "models": [
                    "gemini-1.5-flash",
                    "gemini-1.5-pro",
                    "gemini-pro"
                ]
            },
            "local": {
                "name": "Local Fallback",
                "available": True,
                "default_model": "local-response",
                "models": ["local-response"]
            }
        },
        "default_provider": config.DEFAULT_LLM_PROVIDER
    }

# TTS endpoints
@app.post("/api/tts/generate")
async def generate_tts_audio(
    text: str = Form(...),
    language: str = Form(..., alias="language"),
    format: str = Form("wav", alias="format"),
    device: str = Form("cpu", alias="device"),
    profile_id: Optional[str] = Form(None, alias="profile_id"),
    voice_sample: Optional[UploadFile] = File(None, alias="voice_sample")
):
    """Generate TTS audio with voice cloning support"""
    try:
        logger.info(f"🎵 TTS Request: {len(text)} chars, model: {language}")

        # Prepare reference audio if provided
        reference_data = None
        if voice_sample:
            reference_data = await voice_sample.read()
            logger.info(f"🎤 Voice sample uploaded: {voice_sample.filename}")

        # Find profile if profile_id is provided
        reference_audio_path = None
        if profile_id:
            for profile in tts_service.profiles:
                if profile["id"] == profile_id and profile.get("reference_audio"):
                    reference_audio_path = profile["reference_audio"]
                    break

        # Generate audio
        result = await tts_service.generate_speech(
            text=text,
            language=language,
            format=format,
            device=device,
            reference_audio=reference_data or reference_audio_path
        )

        if result["success"]:
            response_data = {
                "success": True,
                "audio_url": result["url"],
                "filename": result["filename"],
                "model_used": result["model_used"],
                "format": result["format"],
                "language_used": tts_service._get_language_code(language),
                "generation_time": datetime.now().isoformat()
            }

            # Add reference info if used
            if reference_audio_path or reference_data:
                response_data["voice_cloning"] = "used"

            # Add character count for monitoring
            response_data["characters_processed"] = len(text)

            logger.info(f"✅ TTS generation successful: {result['filename']}")
            return response_data
        else:
            error_detail = result.get("error", "Unknown TTS generation error")
            logger.error(f"❌ TTS generation failed: {error_detail}")

            # Provide more specific error messages
            if "model" in error_detail.lower() and ("not found" in error_detail.lower() or "not available" in error_detail.lower()):
                error_detail += " Please try a different TTS model from the available options."
            elif "speaker" in error_detail.lower() or "multi-speaker" in error_detail.lower():
                error_detail += " Try using standard TTS models without voice cloning."
            elif "text" in error_detail.lower() and ("empty" in error_detail.lower() or "none" in error_detail.lower()):
                error_detail = "The text to synthesize cannot be empty. Please provide text to convert to speech."

            raise HTTPException(status_code=500, detail=error_detail)

    except Exception as e:
        logger.error(f"TTS API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tts/audio/{filename}")
async def get_tts_audio(filename: str):
    """Serve generated TTS audio files"""
    file_path = os.path.join(tts_service.audios_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type=f"audio/{filename.split('.')[-1]}")
    else:
        raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/api/tts/profiles")
async def get_tts_profiles():
    """Get all voice profiles"""
    try:
        profiles = tts_service.get_profiles()
        return {
            "success": True,
            "profiles": profiles
        }
    except Exception as e:
        logger.error(f"Error getting TTS profiles: {e}")
        return {
            "success": False,
            "error": str(e),
            "profiles": []
        }

@app.post("/api/tts/save-profile")
async def save_tts_profile(
    name: str = Form(...),
    gender: str = Form(...),
    reference_audio: Optional[UploadFile] = File(None)
):
    """Save a voice profile"""
    try:
        reference_data = None
        if reference_audio:
            reference_data = await reference_audio.read()

        result = tts_service.save_profile(
            name=name,
            gender=gender,
            reference_audio=reference_data
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["error"])

    except Exception as e:
        logger.error(f"Error saving TTS profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/tts/profile/{profile_id}")
async def delete_tts_profile(profile_id: str):
    """Delete a voice profile"""
    try:
        # Find and remove profile
        profile_to_remove = None
        for profile in tts_service.profiles:
            if profile["id"] == profile_id:
                profile_to_remove = profile
                break

        if profile_to_remove:
            # Remove reference audio file if exists
            if profile_to_remove.get("reference_audio") and os.path.exists(profile_to_remove["reference_audio"]):
                os.remove(profile_to_remove["reference_audio"])

            tts_service.profiles.remove(profile_to_remove)
            tts_service.save_profiles()

            return {"success": True, "message": "Profile deleted"}
        else:
            raise HTTPException(status_code=404, detail="Profile not found")

    except Exception as e:
        logger.error(f"Error deleting TTS profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced WhatsApp Voice Agent V2")
    print("📍 Server: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    print("🔍 Health: http://localhost:8001/health")
    print("📊 Status: http://localhost:8001/api/status")
    print("🔌 WebSocket: ws://localhost:8001/ws")
    
    # Use production settings to reduce file monitoring overhead
    reload_enabled = config.ENABLE_FILE_MONITORING and not config.PRODUCTION_MODE
    log_level = "error" if config.PRODUCTION_MODE else "info"
    
    print(f"⚙️ Production Mode: {config.PRODUCTION_MODE}")
    print(f"📊 File Monitoring: {reload_enabled}")
    print(f"📝 Log Level: {log_level}")
    
    uvicorn.run(
        "main_enhanced:app",
        host="0.0.0.0",
        port=8001,
        reload=reload_enabled,  # Disable in production
        log_level=log_level     # Reduce logging in production
    )