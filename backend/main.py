from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import whisper
import torch
import tempfile
import os
import io
import logging
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import json
import time
import uuid
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
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
    message_type: str = "text"  # text, audio
    timestamp: Optional[str] = None

# Classe principal do agente
class VoiceAgent:
    def __init__(self):
        self.whisper_model = None
        self.tts_engine = None
        self.active_connections: List[WebSocket] = []
        self.sessions = {}
        
    async def initialize(self):
        """Inicializa os modelos de STT e TTS"""
        try:
            logger.info("🔄 Carregando modelo Whisper...")
            self.whisper_model = whisper.load_model("base")
            logger.info("✅ Modelo Whisper carregado")
            
            # Simula TTS (em produção usar Coqui TTS)
            logger.info("✅ TTS engine inicializado")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar modelos: {e}")
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcreve áudio para texto usando Whisper"""
        if not self.whisper_model:
            raise HTTPException(status_code=503, detail="Modelo Whisper não carregado")
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file.flush()
                
                result = self.whisper_model.transcribe(temp_file.name, language="pt")
                text = result["text"].strip()
                
                os.unlink(temp_file.name)
                logger.info(f"🎤 Transcrito: {text[:50]}...")
                return text
                
        except Exception as e:
            logger.error(f"❌ Erro na transcrição: {e}")
            raise HTTPException(status_code=500, detail="Erro na transcrição")
    
    async def synthesize_speech(self, text: str) -> bytes:
        """Sintetiza texto para áudio (placeholder - implementar Coqui TTS)"""
        try:
            # Placeholder: retorna áudio vazio por enquanto
            # Em produção, implementar Coqui TTS aqui
            logger.info(f"🔊 Sintetizando: {text[:30]}...")
            
            # Simula processamento TTS
            await asyncio.sleep(0.5)
            
            # Retorna áudio vazio por enquanto
            return b""
            
        except Exception as e:
            logger.error(f"❌ Erro na síntese: {e}")
            raise HTTPException(status_code=500, detail="Erro na síntese de voz")
    
    async def process_message(self, message: str, session_id: str) -> str:
        """Processa mensagem com LLM (placeholder)"""
        try:
            # Placeholder para processamento LLM
            # Em produção, integrar com OpenRouter/Gemini/OpenAI
            
            response = f"Recebi sua mensagem: '{message}'. Como posso ajudá-lo?"
            
            # Simula processamento
            await asyncio.sleep(1)
            
            logger.info(f"🤖 Resposta gerada para sessão {session_id}")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."

# Instância global do agente
agent = VoiceAgent()

# Criar app FastAPI
app = FastAPI(
    title="WhatsApp Voice Agent V2",
    description="Agente de voz para WhatsApp com STT/TTS",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos
import os
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
async def startup_event():
    """Inicializa o agente na inicialização"""
    await agent.initialize()

@app.get("/")
async def read_root():
    """Serve a interface web"""
    template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "index.html")
    return FileResponse(template_path)

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {
        "status": "healthy",
        "whisper_loaded": agent.whisper_model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """Endpoint para Speech-to-Text"""
    try:
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser de áudio")
        
        audio_data = await audio.read()
        text = await agent.transcribe_audio(audio_data)
        
        return {
            "success": True,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro no STT: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """Endpoint para Text-to-Speech"""
    try:
        audio_data = await agent.synthesize_speech(request.text)
        
        # Por enquanto retorna resposta JSON, implementar áudio depois
        return {
            "success": True,
            "message": "TTS processado",
            "text": request.text,
            "audio_size": len(audio_data)
        }
        
    except Exception as e:
        logger.error(f"Erro no TTS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatMessage):
    """Endpoint para chat completo (STT -> LLM -> TTS)"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Processa mensagem
        response_text = await agent.process_message(request.message, session_id)
        
        result = {
            "success": True,
            "session_id": session_id,
            "user_message": request.message,
            "bot_response": response_text,
            "timestamp": datetime.now().isoformat()
        }
        
        # Se TTS habilitado, gera áudio
        if request.use_tts:
            audio_data = await agent.synthesize_speech(response_text)
            result["has_audio"] = True
            result["audio_size"] = len(audio_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/whatsapp/webhook")
async def whatsapp_webhook(message: WhatsAppMessage):
    """Webhook para receber mensagens do WhatsApp"""
    try:
        logger.info(f"📱 Mensagem WhatsApp de {message.from_number}: {message.message}")
        
        # Processa mensagem
        response_text = await agent.process_message(message.message, message.from_number)
        
        # Aqui implementar envio de volta para WhatsApp
        # Por enquanto apenas loga
        logger.info(f"📤 Resposta para {message.from_number}: {response_text}")
        
        return {
            "success": True,
            "response": response_text,
            "to": message.from_number
        }
        
    except Exception as e:
        logger.error(f"Erro no webhook WhatsApp: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para comunicação em tempo real"""
    await websocket.accept()
    agent.active_connections.append(websocket)
    session_id = str(uuid.uuid4())
    
    try:
        await websocket.send_text(json.dumps({
            "type": "connection",
            "session_id": session_id,
            "message": "Conectado ao agente de voz!"
        }))
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                response = await agent.process_message(
                    message_data["message"], 
                    session_id
                )
                
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "message": response,
                    "timestamp": datetime.now().isoformat()
                }))
                
    except WebSocketDisconnect:
        agent.active_connections.remove(websocket)
        logger.info(f"Cliente desconectado: {session_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )