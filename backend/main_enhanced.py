from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
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
import requests
import asyncio
from typing import Optional, List, Dict, Any
import uuid
import time
import sqlite3
from pathlib import Path

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join("..", "logs", "enhanced_agent.log"), encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Import remaining modules
from pydantic import BaseModel
import librosa
import numpy as np

# Configuration Management
class Config:
    def __init__(self):
        self.load_config()
        
    def load_config(self):
        """Load configuration from environment or defaults"""
        # Core API Keys
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCRLSO9lT31tIZgr-hAfgUWNm-9wV7GZ4w")
        self.WHATSAPP_BUSINESS_TOKEN = os.getenv("WHATSAPP_BUSINESS_TOKEN", "")
        self.WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "whatsapp_agent_v2")
        
        # LLM Configuration
        self.DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openrouter")
        self.OPENROUTER_DEFAULT_MODEL = os.getenv("OPENROUTER_DEFAULT_MODEL", "deepseek/deepseek-chat")
        self.GEMINI_DEFAULT_MODEL = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-1.5-flash")
        
        # TTS Configuration  
        self.TTS_ENABLED = os.getenv("TTS_ENABLED", "true").lower() == "true"
        self.TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "pt-BR")
        self.TTS_VOICE = os.getenv("TTS_VOICE", "pt-BR-Wavenet-A")
        
        # Database Configuration
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agent_database.db")
        
        # System Configuration
        self.MAX_AUDIO_SIZE_MB = int(os.getenv("MAX_AUDIO_SIZE_MB", "25"))
        self.MAX_AUDIO_DURATION = int(os.getenv("MAX_AUDIO_DURATION", "300"))
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

# Global configuration
config = Config()

# Pydantic Models
class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    speed: Optional[float] = 1.0
    language: Optional[str] = "pt-BR"

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_tts: Optional[bool] = True
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

# Global variables
whisper_model = None
faster_whisper_model = None
active_connections: List[WebSocket] = []
recent_errors = []

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
        """Generate AI response using specified provider"""
        try:
            provider = provider or config.DEFAULT_LLM_PROVIDER
            
            if provider not in self.providers:
                raise ValueError(f"Unsupported LLM provider: {provider}")
                
            return await self.providers[provider](message, model, system_prompt, max_tokens)
            
        except Exception as e:
            logger.error(f"LLM Service error: {e}")
            return "Desculpe, ocorreu um erro no processamento. Tente novamente."
    
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
        """Call Google Gemini API"""
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
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                raise Exception(f"Gemini API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise
    
    async def _call_local(self, message: str, model: str = None, 
                         system_prompt: str = None, max_tokens: int = 500):
        """Local fallback response"""
        return f"[Local Response] Recebi sua mensagem: '{message}'. Como posso ajudá-lo?"

# TTS Service Integration
class TTSService:
    def __init__(self):
        self.enabled = config.TTS_ENABLED
        
    async def synthesize_speech(self, text: str, voice: str = None, 
                               speed: float = 1.0, language: str = None):
        """Synthesize speech from text"""
        try:
            if not self.enabled:
                return {"success": True, "message": "TTS disabled", "audio_data": None}
            
            voice = voice or config.TTS_VOICE
            language = language or config.TTS_LANGUAGE
            
            logger.info(f"🔊 TTS: Synthesizing '{text[:50]}...' with voice {voice}")
            
            # Try pyttsx3 (offline) or gTTS (online) for actual TTS
            try:
                # Method 1: Try pyttsx3 for offline TTS
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    
                    # Configure for Portuguese if available
                    voices = engine.getProperty('voices')
                    if voices:
                        for v in voices:
                            if 'pt' in v.id.lower() or 'portuguese' in v.name.lower():
                                engine.setProperty('voice', v.id)
                                break
                    
                    engine.setProperty('rate', 150)
                    engine.setProperty('volume', 0.9)
                    
                    # Generate speech to temp file
                    import tempfile
                    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    engine.save_to_file(text, temp_path)
                    engine.runAndWait()
                    
                    # Read audio data
                    with open(temp_path, 'rb') as f:
                        audio_data = f.read()
                    
                    os.unlink(temp_path)  # Cleanup
                    
                    return {
                        "success": True,
                        "message": "TTS generated with pyttsx3",
                        "text": text,
                        "voice": voice,
                        "language": language,
                        "audio_size": len(audio_data),
                        "duration": len(text) / 10,
                        "audio_data": audio_data,
                        "method": "pyttsx3"
                    }
                    
                except Exception as pyttsx3_error:
                    logger.warning(f"pyttsx3 failed: {pyttsx3_error}")
                
                # Method 2: Try gTTS for online TTS
                try:
                    from gtts import gTTS
                    import tempfile
                    
                    lang_code = 'pt' if language.startswith('pt') else 'en'
                    tts = gTTS(text=text, lang=lang_code, slow=False)
                    
                    temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    tts.save(temp_path)
                    
                    with open(temp_path, 'rb') as f:
                        audio_data = f.read()
                    
                    os.unlink(temp_path)  # Cleanup
                    
                    return {
                        "success": True,
                        "message": "TTS generated with gTTS",
                        "text": text,
                        "voice": voice,
                        "language": language,
                        "audio_size": len(audio_data),
                        "duration": len(text) / 10,
                        "audio_data": audio_data,
                        "method": "gTTS"
                    }
                    
                except Exception as gtts_error:
                    logger.warning(f"gTTS failed: {gtts_error}")
                
                # Fallback: Simulate processing
                await asyncio.sleep(0.5)
                
            except ImportError:
                # TTS libraries not installed
                await asyncio.sleep(0.5)  # Simulate processing
            
            return {
                "success": True,
                "message": "TTS processed (text-only mode)",
                "text": text,
                "voice": voice,
                "language": language,
                "audio_size": len(text) * 10,  # Simulated size
                "duration": len(text) / 10,   # Simulated duration
                "audio_data": None,  # No actual audio
                "method": "simulation"
            }
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return {"success": False, "error": str(e)}

# Database Service Integration
class DatabaseService:
    def __init__(self):
        self.db_path = "agent_database.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
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
            
            logger.info("✅ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def save_conversation(self, session_id: str, user_message: str, 
                         assistant_response: str, llm_provider: str = None, 
                         llm_model: str = None, processing_time: float = None):
        """Save conversation to database"""
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

# Initialize services
llm_service = LLMService()
tts_service = TTSService()
db_service = DatabaseService()

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Voice Agent V2 - Enhanced Version",
    description="Complete voice agent with LLM integration, TTS, and database support",
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

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    logger.info(f"🔍 {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"✅ {response.status_code} in {process_time:.2f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"💥 Request failed after {process_time:.2f}s: {str(e)}")
        raise

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
                                <li>🔊 <strong>TTS Support</strong> - Text-to-speech synthesis</li>
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
            "tts_service": {
                "status": "healthy" if tts_service.enabled else "disabled",
                "enabled": tts_service.enabled,
                "language": config.TTS_LANGUAGE
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

# Enhanced TTS endpoint
@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Enhanced TTS endpoint"""
    try:
        result = await tts_service.synthesize_speech(
            text=request.text,
            voice=request.voice,
            speed=request.speed,
            language=request.language
        )
        
        logger.info(f"🔊 TTS processed: '{request.text[:30]}...'")
        return result
        
    except Exception as e:
        logger.error(f"TTS Error: {e}")
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
            "model": request.model or config.OPENROUTER_DEFAULT_MODEL,
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
        
        # Add TTS if requested
        if request.use_tts:
            tts_result = await tts_service.synthesize_speech(response_text)
            if tts_result["success"]:
                result["has_audio"] = True
                result["audio_size"] = tts_result.get("audio_size", 0)
                result["tts_info"] = tts_result
        
        logger.info(f"💬 Chat completed for session {session_id}")
        return result
        
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
                "tts": "ready" if tts_service.enabled else "disabled",
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
                
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "message": response,
                    "provider": provider,
                    "timestamp": datetime.now().isoformat()
                }))
                
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
            "tts_service": "enabled" if tts_service.enabled else "disabled",
            "database": "ready"
        },
        "configuration": {
            "default_llm_provider": config.DEFAULT_LLM_PROVIDER,
            "tts_enabled": config.TTS_ENABLED,
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

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced WhatsApp Voice Agent V2")
    print("📍 Server: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    print("🔍 Health: http://localhost:8001/health")
    print("📊 Status: http://localhost:8001/api/status")
    print("🔌 WebSocket: ws://localhost:8001/ws")
    
    uvicorn.run(
        "main_enhanced:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )