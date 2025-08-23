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

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for maximum detail
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Console output
        logging.FileHandler(os.path.join("..", "logs", "stt_debug.log"), encoding='utf-8')  # File output
    ]
)
logger = logging.getLogger(__name__)

# Import remaining modules
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import json
import time
import uuid
import librosa
import numpy as np

# Global error tracking
recent_errors = []

# Pydantic Models
class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "default"
    speed: Optional[float] = 1.0

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_tts: Optional[bool] = True

class WhatsAppMessage(BaseModel):
    from_number: str
    message: str
    message_type: str = "text"
    timestamp: Optional[str] = None

# Global variables
whisper_model = None
faster_whisper_model = None
active_connections: List[WebSocket] = []

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Voice Agent V2 - Working Version",
    description="Simple and working version of WhatsApp Voice Agent with STT",
    version="2.0.3-working"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    
    # Log request details
    logger.info(f"🔍 Incoming request: {request.method} {request.url}")
    logger.info(f"   Headers: {dict(request.headers)}")
    
    if request.method == "POST" and str(request.url).endswith("/api/stt"):
        logger.info(f"🎤 STT Request received")
        logger.info(f"   Content-Type: {request.headers.get('content-type', 'Not specified')}")
        logger.info(f"   Content-Length: {request.headers.get('content-length', 'Not specified')}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response details
        logger.info(f"✅ Response: {response.status_code} in {process_time:.2f}s")
        
        if response.status_code >= 400:
            logger.error(f"❌ Error response: {response.status_code}")
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"💥 Request failed after {process_time:.2f}s: {str(e)}")
        logger.exception("Full exception details:")
        raise

# Load Whisper model on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Whisper models"""
    global whisper_model, faster_whisper_model
    try:
        logger.info("🔄 Loading faster-whisper model (better codec support)...")
        faster_whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        logger.info("✅ faster-whisper model loaded successfully")
        
        # Keep openai-whisper as fallback
        logger.info("🔄 Loading openai-whisper as fallback...")
        whisper_model = whisper.load_model("base")
        logger.info("✅ openai-whisper fallback loaded")
        
    except Exception as e:
        logger.error(f"❌ Failed to load Whisper models: {e}")

# Root endpoint - serve the interface
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main interface"""
    try:
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "index.html")
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return HTMLResponse(content="""
                <html>
                    <head><title>WhatsApp Voice Agent V2</title></head>
                    <body>
                        <h1>🤖 WhatsApp Voice Agent V2</h1>
                        <p>Server is running but interface file not found.</p>
                        <a href="/health">Check Health</a> |
                        <a href="/docs">API Docs</a>
                    </body>
                </html>
            """)
    except Exception as e:
        logger.error(f"Error serving root: {e}")
        return HTMLResponse(content=f"<h1>Error: {e}</h1>")

# Favicon endpoint to fix 404 errors
@app.get("/favicon.ico")
async def favicon():
    """Simple favicon response to prevent 404 errors"""
    return Response(content="", media_type="image/x-icon")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "whisper_loaded": whisper_model is not None,
        "faster_whisper_loaded": faster_whisper_model is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.3-faster-whisper"
    }

# STT endpoint - Fixed version with proper Windows file handling
@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """Fixed Speech-to-Text endpoint with proper Windows file handling"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"\n🎤 [{request_id}] STT Request started")
    logger.info(f"   Audio filename: {audio.filename}")
    logger.info(f"   Content-type: {audio.content_type}")
    
    temp_file = None
    
    try:
        # Step 1: Validate request
        if not faster_whisper_model and not whisper_model:
            logger.error(f"❌ [{request_id}] No Whisper models loaded")
            raise HTTPException(status_code=503, detail="Whisper models not loaded")
        
        # Step 2: Read audio data
        logger.info(f"📊 [{request_id}] Reading audio data")
        audio_data = await audio.read()
        logger.info(f"   Audio data size: {len(audio_data)} bytes")
        
        if len(audio_data) == 0:
            logger.error(f"❌ [{request_id}] Empty audio file")
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Step 3: Detect actual audio format and create proper temp file
        logger.info(f"🔍 [{request_id}] Detecting audio format")
        
        # Read first few bytes to detect format
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
        elif audio_header.startswith(b'fLaC'):
            detected_format = 'flac'
            file_extension = '.flac'
        else:
            # Default to webm as it's most common from browsers
            detected_format = 'webm'
            file_extension = '.webm'
            logger.warning(f"⚠️ [{request_id}] Unknown format, assuming WebM")
        
        logger.info(f"   Detected format: {detected_format}")
        
        # Create temp file with proper extension
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(
            suffix=file_extension, 
            delete=False,
            dir=os.path.join(os.getcwd(), "temp_audio")
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(temp_file.name), exist_ok=True)
        
        # Write audio data and ensure it's flushed
        temp_file.write(audio_data)
        temp_file.flush()
        os.fsync(temp_file.fileno())  # Force write to disk
        temp_file.close()  # Close handle before processing
        
        temp_path = temp_file.name
        normalized_path = os.path.normpath(temp_path)
        logger.info(f"   Temp file created: {temp_path}")
        logger.info(f"   Normalized path: {normalized_path}")
        logger.info(f"   File size: {os.path.getsize(temp_path)} bytes")
        
        # Verify file exists and is readable
        if not os.path.exists(normalized_path):
            raise FileNotFoundError(f"Temp file not found: {normalized_path}")
            
        if not os.access(normalized_path, os.R_OK):
            raise PermissionError(f"Cannot read temp file: {normalized_path}")
        
        # Step 4: Wait a moment for Windows file system
        import time
        time.sleep(0.1)  # Brief pause for Windows FS
        
        # Step 5: Transcription with proper error handling
        logger.info(f"🎤 [{request_id}] Starting transcription")
        start_time = time.time()
        
        try:
            # Method 1: Use faster-whisper (best codec support for WebM)
            if faster_whisper_model:
                logger.info(f"🔄 [{request_id}] Method 1: faster-whisper (superior WebM support)")
                
                try:
                    # faster-whisper can handle WebM, OGG, WAV directly
                    logger.info(f"   Transcribing {detected_format} with faster-whisper")
                    segments, info = faster_whisper_model.transcribe(
                        normalized_path, 
                        language="pt"
                    )
                    
                    # Convert segments to text
                    text_segments = list(segments)
                    transcribed_text = " ".join([segment.text for segment in text_segments]).strip()
                    
                    # Create result object compatible with openai-whisper format
                    result = {
                        "text": transcribed_text,
                        "language": info.language,
                        "language_probability": info.language_probability,
                        "duration": info.duration,
                        "segments": [{"text": seg.text, "start": seg.start, "end": seg.end} for seg in text_segments]
                    }
                    
                    transcription_method = f"faster_whisper_{detected_format}"
                    logger.info(f"✅ [{request_id}] faster-whisper transcription successful")
                    logger.info(f"   Language: {info.language} (confidence: {info.language_probability:.2f})")
                    logger.info(f"   Duration: {info.duration:.2f}s")
                    logger.info(f"   Text: '{transcribed_text[:100]}{'...' if len(transcribed_text) > 100 else ''}'")
                    
                except Exception as faster_whisper_error:
                    logger.warning(f"⚠️ [{request_id}] faster-whisper failed: {str(faster_whisper_error)}")
                    raise faster_whisper_error
            else:
                raise Exception("faster-whisper model not available")
            
        except Exception as faster_whisper_error:
            logger.warning(f"⚠️ [{request_id}] faster-whisper method failed: {str(faster_whisper_error)}")
            
            try:
                # Method 2: Fallback to librosa + openai-whisper
                logger.info(f"🔄 [{request_id}] Method 2: Librosa + openai-whisper fallback")
                
                import librosa
                
                # Load with librosa and process with openai-whisper
                audio_np, sr = librosa.load(normalized_path, sr=16000)
                logger.info(f"   Loaded audio: shape={audio_np.shape}, sr={sr}")
                
                if len(audio_np) == 0:
                    raise ValueError("Audio array is empty")
                
                result = whisper_model.transcribe(
                    audio_np,
                    language="pt",
                    fp16=False,
                    verbose=False
                )
                transcription_method = f"librosa_fallback_{detected_format}"
                logger.info(f"✅ [{request_id}] Fallback transcription successful")
                
            except Exception as fallback_error:
                logger.error(f"❌ [{request_id}] All transcription methods failed:")
                logger.error(f"   faster-whisper: {str(faster_whisper_error)}")
                logger.error(f"   Fallback: {str(fallback_error)}")
                
                raise HTTPException(
                    status_code=500,
                    detail=f"STT failed. Format: {detected_format}. See logs for details."
                )
        
        # Step 6: Process transcription results
        processing_time = time.time() - start_time
        text = result["text"].strip() if result and "text" in result else ""
        
        logger.info(f"📋 [{request_id}] Processing results")
        logger.info(f"   Method used: {transcription_method}")
        logger.info(f"   Processing time: {processing_time:.2f}s")
        logger.info(f"   Text length: {len(text)} chars")
        logger.info(f"   Transcribed text: '{text[:100]}{'...' if len(text) > 100 else ''}'")
        
        # Handle empty transcription
        if not text:
            text = "[Áudio não foi reconhecido como fala ou estava muito baixo]"
            logger.warning(f"⚠️ [{request_id}] Empty transcription - using default message")
        
        # Prepare response
        response_data = {
            "success": True,
            "text": text,
            "confidence": 0.95,
            "processing_time": processing_time,
            "transcription_method": transcription_method,
            "request_id": request_id,
            "audio_duration": result.get("segments", [{}])[-1].get("end", 0) if result and result.get("segments") else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ [{request_id}] STT Request completed successfully")
        return response_data
        
    except HTTPException as http_err:
        logger.error(f"❌ [{request_id}] HTTP Exception: {http_err.status_code} - {http_err.detail}")
        raise
    except Exception as e:
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "audio_filename": getattr(audio, 'filename', 'unknown')
        }
        recent_errors.append(error_info)
        # Keep only last 10 errors
        if len(recent_errors) > 10:
            recent_errors.pop(0)
            
        logger.error(f"💥 [{request_id}] CRITICAL ERROR in STT processing")
        logger.error(f"   Error type: {type(e).__name__}")
        logger.error(f"   Error message: {str(e)}")
        logger.exception(f"[{request_id}] Full traceback:")
        raise HTTPException(status_code=500, detail=f"STT processing failed: {str(e)}")
    
    finally:
        # Cleanup with proper Windows handling
        logger.info(f"🧹 [{request_id}] Starting cleanup")
        
        if 'temp_file' in locals() and temp_file and hasattr(temp_file, 'name'):
            temp_path = temp_file.name
            try:
                if os.path.exists(temp_path):
                    # Ensure file is not locked before deletion
                    import time
                    time.sleep(0.1)
                    os.unlink(temp_path)
                    logger.info(f"   ✅ Cleaned up temp file: {os.path.basename(temp_path)}")
            except Exception as e:
                logger.warning(f"   ⚠️ Failed to cleanup temp file: {e}")
        
        logger.info(f"🧹 [{request_id}] Cleanup completed")

# TTS endpoint
@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Text-to-Speech endpoint (placeholder)"""
    try:
        logger.info(f"🔊 TTS request: {request.text[:30]}...")
        
        return {
            "success": True,
            "message": "TTS processed successfully",
            "text": request.text,
            "voice": request.voice,
            "audio_size": len(request.text) * 10,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatMessage):
    """Chat endpoint with AI processing"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Simple AI response
        response_text = f"Recebi sua mensagem: '{request.message}'. Como posso ajudá-lo hoje?"
        
        await asyncio.sleep(0.5)
        
        result = {
            "success": True,
            "session_id": session_id,
            "user_message": request.message,
            "bot_response": response_text,
            "timestamp": datetime.now().isoformat()
        }
        
        if request.use_tts:
            result["has_audio"] = True
            result["audio_size"] = len(response_text) * 10
        
        logger.info(f"💬 Chat response generated for session {session_id}")
        return result
        
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WhatsApp webhook endpoint
@app.post("/api/whatsapp/webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    """WhatsApp webhook endpoint"""
    try:
        logger.info(f"📱 WhatsApp message from {message.from_number}: {message.message}")
        
        response_text = f"Olá! Recebi sua mensagem: '{message.message}'. Sou um assistente virtual!"
        
        await asyncio.sleep(1)
        
        logger.info(f"📤 Response to {message.from_number}: {response_text[:50]}...")
        
        return {
            "success": True,
            "response": response_text,
            "to": message.from_number,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"WhatsApp Webhook Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections.append(websocket)
    session_id = str(uuid.uuid4())
    
    try:
        await websocket.send_text(json.dumps({
            "type": "connection",
            "session_id": session_id,
            "message": "🤖 Conectado ao agente de voz!"
        }))
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                user_message = message_data["message"]
                response = f"Recebi: '{user_message}'. Como posso ajudar?"
                
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "message": response,
                    "timestamp": datetime.now().isoformat()
                }))
                
                logger.info(f"🔌 WebSocket chat: {user_message[:30]}...")
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"🔌 WebSocket disconnected: {session_id}")

@app.get("/api/errors")
async def get_recent_errors():
    """Get recent STT errors for debugging"""
    return {
        "recent_errors": recent_errors,
        "total_count": len(recent_errors),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/temp_files")
async def get_temp_files():
    """List temporary files for debugging"""
    try:
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        if os.path.exists(temp_dir):
            files = []
            for filename in os.listdir(temp_dir):
                filepath = os.path.join(temp_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    files.append({
                        "filename": filename,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
                    })
            return {"temp_files": files, "count": len(files)}
        else:
            return {"temp_files": [], "count": 0}
    except Exception as e:
        return {"error": str(e)}

# Status endpoint
@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "server": "running",
        "whisper_model": "loaded" if whisper_model else "not_loaded",
        "active_connections": len(active_connections),
        "version": "2.0.3-working",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "API is working!",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting WhatsApp Voice Agent V2 - Working Version")
    print("📍 Server will be available at: http://localhost:8001")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )