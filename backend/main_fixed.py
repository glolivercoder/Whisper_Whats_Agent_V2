from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import os
import logging
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import json
import time
import uuid
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
active_connections: List[WebSocket] = []

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Voice Agent V2 - Fixed",
    description="Fixed version of WhatsApp Voice Agent with working endpoints",
    version="2.0.1"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Whisper model"""
    global whisper_model
    try:
        logger.info("🔄 Loading Whisper model...")
        whisper_model = whisper.load_model("base")
        logger.info("✅ Whisper model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load Whisper model: {e}")

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
                        <p>Template path: {}</p>
                        <a href="/health">Check Health</a> |
                        <a href="/docs">API Docs</a>
                    </body>
                </html>
            """.format(template_path))
    except Exception as e:
        logger.error(f"Error serving root: {e}")
        return HTMLResponse(content=f"<h1>Error: {e}</h1>")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "whisper_loaded": whisper_model is not None,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.1-fixed"
    }

# STT endpoint
@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """Speech-to-Text endpoint with robust Windows file handling"""
    temp_file_path = None
    try:
        # Validate audio file
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be audio format")
        
        if not whisper_model:
            raise HTTPException(status_code=503, detail="Whisper model not loaded")
        
        logger.info(f"📥 Received audio file: {audio.filename}, type: {audio.content_type}")
        
        # Read audio data
        audio_data = await audio.read()
        logger.info(f"📊 Audio data size: {len(audio_data)} bytes")
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Create dedicated temp directory for audio files
        import os
        temp_dir = os.path.join(os.getcwd(), "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create unique filename with timestamp
        import time
        timestamp = int(time.time() * 1000)
        temp_file_path = os.path.join(temp_dir, f"whisper_audio_{timestamp}.wav")
        
        # Write audio data directly to file
        with open(temp_file_path, 'wb') as f:
            f.write(audio_data)
            f.flush()
            os.fsync(f.fileno())  # Force write to disk
        
        logger.info(f"💾 Saved audio to temp file: {temp_file_path}")
        
        # Verify file exists and has content
        if not os.path.exists(temp_file_path):
            raise HTTPException(status_code=500, detail="Failed to create temporary file")
        
        file_size = os.path.getsize(temp_file_path)
        logger.info(f"📏 Temp file size: {file_size} bytes")
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Temporary file is empty")
        
        # Wait a bit to ensure file is fully written (Windows)
        time.sleep(0.2)
        
        # Transcribe audio with error handling
        logger.info("🎤 Starting transcription...")
        start_time = time.time()
        
        # Use absolute path and verify it exists before transcription
        abs_temp_path = os.path.abspath(temp_file_path)
        logger.info(f"🔍 Attempting transcription of: {abs_temp_path}")
        
        # Double-check file exists and is accessible
        if not os.path.exists(abs_temp_path):
            raise HTTPException(status_code=500, detail=f"Audio file not accessible: {abs_temp_path}")
        
        try:
            # Test file access by opening it
            with open(abs_temp_path, 'rb') as test_file:
                test_data = test_file.read(100)  # Read first 100 bytes
                if len(test_data) == 0:
                    raise Exception("File is empty or not readable")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File access error: {str(e)}")
        
        # Perform Whisper transcription
        try:
            result = whisper_model.transcribe(
                abs_temp_path, 
                language="pt",
                fp16=False,  # Use FP32 for CPU compatibility
                verbose=False  # Reduce output verbosity
            )
        except Exception as whisper_error:
            logger.error(f"❌ Whisper transcription error: {whisper_error}")
            
            # Try alternative approach: load audio into numpy array first
            try:
                import librosa
                audio_np, sr = librosa.load(abs_temp_path, sr=16000)
                result = whisper_model.transcribe(audio_np, language="pt", fp16=False)
                logger.info("✅ Transcription successful using numpy array approach")
            except Exception as alt_error:
                raise HTTPException(status_code=500, detail=f"Transcription failed with both methods: {str(whisper_error)}, {str(alt_error)}")
        
        processing_time = time.time() - start_time
        text = result["text"].strip()
        
        logger.info(f"✅ Transcription completed in {processing_time:.2f}s")
        logger.info(f"📝 Transcribed text: '{text[:100]}...'")        
        
        return {
                "success": True,
                "text": text,
                "confidence": 0.95,  # Placeholder
                "processing_time": processing_time,
                "audio_duration": result.get("segments", [{}])[-1].get("end", 0) if result.get("segments") else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as transcription_error:
            logger.error(f"❌ File handling error: {transcription_error}")
            raise HTTPException(status_code=500, detail=f"File processing failed: {str(transcription_error)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ STT Error: {e}")
        raise HTTPException(status_code=500, detail=f"STT processing failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"🧹 Cleaned up temp file: {temp_file_path}")
            except Exception as cleanup_error:
                logger.warning(f"⚠️ Failed to cleanup temp file: {cleanup_error}")

# TTS endpoint
@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Text-to-Speech endpoint (placeholder)"""
    try:
        logger.info(f"🔊 TTS request: {request.text[:30]}...")
        
        # Placeholder TTS - return success for now
        return {
            "success": True,
            "message": "TTS processed successfully",
            "text": request.text,
            "voice": request.voice,
            "audio_size": len(request.text) * 10,  # Placeholder
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
        
        # Simple AI response (placeholder for LLM)
        response_text = f"Recebi sua mensagem: '{request.message}'. Como posso ajudá-lo hoje?"
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        result = {
            "success": True,
            "session_id": session_id,
            "user_message": request.message,
            "bot_response": response_text,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add TTS info if enabled
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
        
        # Process message (placeholder for AI processing)
        response_text = f"Olá! Recebi sua mensagem: '{message.message}'. Sou um assistente virtual e estou aqui para ajudar!"
        
        # Simulate processing
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
        # Send welcome message
        await websocket.send_text(json.dumps({
            "type": "connection",
            "session_id": session_id,
            "message": "🤖 Conectado ao agente de voz! Envie mensagens ou áudio."
        }))
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                # Process chat message
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

# Additional utility endpoints
@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "server": "running",
        "whisper_model": "loaded" if whisper_model else "not_loaded",
        "active_connections": len(active_connections),
        "version": "2.0.1-fixed",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "API is working!",
        "timestamp": datetime.now().isoformat()
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting WhatsApp Voice Agent V2 - Fixed Version")
    print("📍 Server will be available at: http://localhost:8001")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    
    uvicorn.run(
        "main_fixed:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )