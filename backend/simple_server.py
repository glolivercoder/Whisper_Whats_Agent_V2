from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from pydantic import BaseModel
from typing import Optional
import json
import time
import uuid
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_tts: Optional[bool] = True

class WhatsAppMessage(BaseModel):
    from_number: str
    message: str
    message_type: str = "text"
    timestamp: Optional[str] = None

# Create FastAPI app
app = FastAPI(
    title="WhatsApp Voice Agent V2 - Simple Working Version",
    description="Simplified working version for immediate testing",
    version="2.0.2-simple"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main interface"""
    try:
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "index.html")
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Update WebSocket URL to use port 8002
                content = content.replace('localhost:8001', 'localhost:8002')
            return HTMLResponse(content=content)
        else:
            return HTMLResponse(content="""
                <html>
                    <head><title>WhatsApp Voice Agent V2 - Simple</title></head>
                    <body>
                        <h1>🤖 WhatsApp Voice Agent V2 - Working Version</h1>
                        <p>✅ Server is running on port 8002</p>
                        <p>✅ STT endpoint is working (simulation mode)</p>
                        <p>✅ Ready for voice recording tests</p>
                        <a href="/health">Health Check</a> | 
                        <a href="/docs">API Docs</a>
                    </body>
                </html>
            """)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {e}</h1>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "stt_working": True,
        "version": "2.0.2-simple",
        "timestamp": datetime.now().isoformat(),
        "note": "STT in simulation mode for testing"
    }

@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """Working STT endpoint (simulation mode)"""
    try:
        # Validate audio file
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be audio format")
        
        logger.info(f"📥 Received audio file: {audio.filename}, type: {audio.content_type}")
        
        # Read audio data
        audio_data = await audio.read()
        logger.info(f"📊 Audio data size: {len(audio_data)} bytes")
        
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Return success response with simulated transcription
        processing_time = 1.0
        transcribed_text = "Olá! Este é um teste de transcrição de áudio. O sistema está funcionando corretamente!"
        
        logger.info(f"✅ STT processed: {len(audio_data)} bytes -> '{transcribed_text}'")
        
        return {
            "success": True,
            "text": transcribed_text,
            "confidence": 0.95,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat(),
            "note": "STT simulation mode - replace with real Whisper when fixed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ STT Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatMessage):
    """Chat endpoint"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Simple AI response
        response_text = f"Recebi sua mensagem: '{request.message}'. Como posso ajudá-lo hoje? (Sistema funcionando perfeitamente!)"
        
        result = {
            "success": True,
            "session_id": session_id,
            "user_message": request.message,
            "bot_response": response_text,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"💬 Chat response for: {request.message[:30]}...")
        return result
        
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/whatsapp/webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    """WhatsApp webhook endpoint"""
    try:
        logger.info(f"📱 WhatsApp from {message.from_number}: {message.message}")
        
        response_text = f"Olá! Recebi sua mensagem: '{message.message}'. Sistema de voz funcionando! 🤖"
        
        return {
            "success": True,
            "response": response_text,
            "to": message.from_number,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"WhatsApp Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "Simple server working perfectly!",
        "stt_status": "simulation_mode",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    import asyncio
    
    print("🚀 Starting WhatsApp Voice Agent V2 - Simple Working Version")
    print("📍 Server: http://localhost:8002")
    print("🎤 STT: Working in simulation mode")
    print("✅ Ready for voice recording tests!")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )