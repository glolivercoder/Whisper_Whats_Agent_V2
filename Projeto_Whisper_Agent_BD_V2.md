# Projeto Whisper Agent BD V2 - Sistema Híbrido com Interface Avançada

## Visão Geral

Sistema de atendimento automatizado **híbrido** que combina a interface web avançada do projeto de referência com backend robusto para banco de dados, usando Whisper FastAPI para STT, Coqui TTS para síntese de voz e agentes LLM para interação inteligente com clientes.

## Objetivos

- ✅ **Interface Web Avançada** - Baseada no projeto de referência com React/Vite
- ✅ **Whisper FastAPI** - STT de alta performance e baixa latência
- ✅ **Coqui TTS** - Síntese de voz open source de qualidade
- ✅ **Agentes LLM Flexíveis** - OpenRouter, Gemini, OpenAI
- ✅ **Banco de Dados Universal** - Conecta com qualquer aplicação existente
- ✅ **Sistema Híbrido** - Frontend moderno + Backend robusto
- ✅ **Integração Completa** - STT → LLM → DB → TTS em tempo real

## Arquitetura Híbrida

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND AVANÇADO (React/Vite)              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  • Interface de Voz Inteligente                           │ │
│  │  • Seletor de Modelos LLM (OpenRouter/Gemini)            │ │
│  │  • Configuração de Vozes TTS                             │ │
│  │  • Painel de Diagnósticos                                │ │
│  │  • Leitor de PDF com IA                                  │ │
│  │  • Sistema de Logs Avançado                              │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ WebSocket + REST API
┌─────────────────────▼───────────────────────────────────────────┐
│                 GATEWAY HÍBRIDO (FastAPI)                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  • Roteamento Inteligente                                 │ │
│  │  • WebSocket Manager                                      │ │
│  │  • Autenticação & Rate Limiting                          │ │
│  │  • Proxy para Serviços                                   │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─┬─────────────┬─────────────┬─────────────┬───────────────────────┘
  │             │             │             │
┌─▼─────────┐ ┌─▼─────────┐ ┌─▼─────────┐ ┌─▼─────────────────────┐
│ WHISPER   │ │ COQUI TTS │ │ LLM AGENT │ │ DATABASE CONNECTOR    │
│ FastAPI   │ │ FastAPI   │ │ FastAPI   │ │ Universal Adapter     │
│ (STT)     │ │ (TTS)     │ │ Multi-LLM │ │ (MySQL/PG/Oracle/etc) │
└───────────┘ └───────────┘ └───────────┘ └─────────────────────────┘
```## 
Estrutura do Projeto Híbrido

```
whisper_agent_bd_v2/
├── frontend/                    # Interface Web Avançada (React/Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioWeaviteInterface.jsx    # Interface principal de voz
│   │   │   ├── AIModelSelector.jsx          # Seletor de modelos LLM
│   │   │   ├── GeminiVoiceSelector.jsx      # Seletor de vozes Gemini
│   │   │   ├── VoiceConfigPanel.jsx         # Painel de configuração
│   │   │   ├── ConversationFlow.jsx         # Fluxo de conversação
│   │   │   ├── PDFTextReader.jsx            # Leitor de PDF com IA
│   │   │   ├── DiagnosticsPanel.jsx         # Painel de diagnósticos
│   │   │   ├── DatabaseConnector.jsx        # Interface de conexão DB
│   │   │   └── AIStatusRobot.jsx            # Status visual do sistema
│   │   ├── services/
│   │   │   ├── geminiSpeechService.js       # Serviço Gemini TTS/STT
│   │   │   ├── openRouterService.js         # Serviço OpenRouter
│   │   │   ├── googleAIService.js           # Serviço Google AI
│   │   │   ├── pdfService.js                # Processamento PDF
│   │   │   ├── envService.js                # Gerenciamento de env
│   │   │   └── databaseService.js           # Cliente para backend DB
│   │   ├── hooks/
│   │   │   ├── useVoiceAgent.js             # Hook principal de voz
│   │   │   ├── useAgentModel.js             # Hook para modelos LLM
│   │   │   ├── useVoiceConfig.js            # Hook de configuração
│   │   │   ├── useVoiceRecognition.js       # Hook de reconhecimento
│   │   │   ├── useAudioDevices.js           # Hook de dispositivos
│   │   │   └── useDatabaseConnection.js     # Hook para conexão DB
│   │   ├── utils/
│   │   │   ├── audioUtils.js                # Utilitários de áudio
│   │   │   ├── languageUtils.js             # Utilitários de idioma
│   │   │   └── logger.js                    # Sistema de logs
│   │   └── styles/
│   │       ├── App.css                      # Estilos principais
│   │       ├── VoiceConfigPanel.css         # Estilos do painel
│   │       └── index.css                    # Estilos globais
│   ├── package.json                         # Dependências frontend
│   ├── vite.config.js                       # Configuração Vite
│   └── index.html                           # HTML principal
├── backend/                     # Backend Híbrido (FastAPI)
│   ├── services/
│   │   ├── gateway/             # Gateway Principal
│   │   │   ├── main.py         # FastAPI gateway
│   │   │   ├── websocket.py    # WebSocket manager
│   │   │   ├── routes.py       # Rotas da API
│   │   │   └── middleware.py   # Middlewares
│   │   ├── whisper_stt/        # Serviço Whisper STT
│   │   │   ├── main.py         # Whisper FastAPI
│   │   │   ├── whisper_model.py # Modelo Whisper
│   │   │   └── audio_processor.py # Processamento áudio
│   │   ├── coqui_tts/          # Serviço Coqui TTS
│   │   │   ├── main.py         # Coqui FastAPI
│   │   │   ├── tts_engine.py   # Engine TTS
│   │   │   └── voice_manager.py # Gerenciador de vozes
│   │   ├── llm_agent/          # Agente LLM Multi-Provider
│   │   │   ├── main.py         # LLM FastAPI
│   │   │   ├── openrouter_client.py # Cliente OpenRouter
│   │   │   ├── gemini_client.py     # Cliente Gemini
│   │   │   ├── openai_client.py     # Cliente OpenAI
│   │   │   └── agent_orchestrator.py # Orquestrador
│   │   └── database/           # Conector Universal de Banco
│   │       ├── main.py         # Database FastAPI
│   │       ├── universal_connector.py # Conector universal
│   │       ├── query_builder.py      # Construtor de queries
│   │       ├── schema_analyzer.py    # Analisador de schema
│   │       └── security_validator.py # Validador de segurança
│   ├── shared/                 # Código Compartilhado
│   │   ├── config.py           # Configurações globais
│   │   ├── models.py           # Modelos Pydantic
│   │   ├── exceptions.py       # Exceções customizadas
│   │   └── utils.py            # Utilitários
│   └── requirements/           # Dependências por serviço
│       ├── gateway.txt         # Deps gateway
│       ├── whisper.txt         # Deps Whisper
│       ├── coqui.txt           # Deps Coqui
│       ├── llm.txt             # Deps LLM
│       └── database.txt        # Deps Database
├── docker/                     # Containerização
│   ├── docker-compose.yml      # Orquestração completa
│   ├── gateway.Dockerfile      # Gateway container
│   ├── whisper.Dockerfile      # Whisper container
│   ├── coqui.Dockerfile        # Coqui container
│   ├── llm.Dockerfile          # LLM container
│   ├── database.Dockerfile     # Database connector
│   └── nginx.conf              # Proxy reverso
├── models/                     # Modelos Locais
│   ├── whisper/               # Modelos Whisper
│   ├── coqui/                 # Modelos Coqui TTS
│   └── embeddings/            # Modelos de embedding
├── scripts/                   # Scripts de Automação
│   ├── setup.sh              # Setup completo
│   ├── download_models.sh     # Download de modelos
│   ├── start_dev.sh           # Desenvolvimento
│   └── deploy.sh              # Deploy produção
├── tests/                     # Testes
│   ├── frontend/              # Testes frontend
│   ├── backend/               # Testes backend
│   └── integration/           # Testes integração
├── docs/                      # Documentação
│   ├── API.md                 # Documentação da API
│   ├── DEPLOYMENT.md          # Guia de deploy
│   └── CONFIGURATION.md       # Guia de configuração
├── .env.example               # Exemplo de configuração
├── docker-compose.dev.yml     # Desenvolvimento
└── README.md                  # Documentação principal
```## Im
plementação Detalhada

### 1. Configuração Global (backend/shared/config.py)

```python
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any
import os

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Services Configuration
    GATEWAY_HOST: str = "0.0.0.0"
    GATEWAY_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"  # Vite dev server
    
    # Internal Services URLs
    WHISPER_SERVICE_URL: str = "http://whisper-stt:8001"
    COQUI_SERVICE_URL: str = "http://coqui-tts:8002"
    LLM_SERVICE_URL: str = "http://llm-agent:8003"
    DATABASE_SERVICE_URL: str = "http://database-connector:8004"
    
    # Whisper STT Configuration
    WHISPER_MODEL_SIZE: str = "base"  # tiny, base, small, medium, large
    WHISPER_LANGUAGE: str = "pt"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"  # int8, float16, float32
    
    # Coqui TTS Configuration
    COQUI_MODEL_NAME: str = "tts_models/pt/cv/vits"
    COQUI_VOCODER: Optional[str] = None
    COQUI_SPEAKER_IDX: Optional[int] = None
    COQUI_LANGUAGE: str = "pt"
    
    # LLM Configuration (Multi-Provider)
    DEFAULT_LLM_PROVIDER: str = "openrouter"  # openrouter, gemini, openai
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "deepseek/deepseek-chat"
    
    # Gemini Configuration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_DEFAULT_MODEL: str = "gemini-1.5-flash"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_DEFAULT_MODEL: str = "gpt-3.5-turbo"
    
    # Database Configuration (Universal)
    DATABASE_CONNECTIONS: Dict[str, Dict[str, Any]] = {}
    MAX_CONNECTIONS_PER_DB: int = 5
    CONNECTION_TIMEOUT: int = 30
    QUERY_TIMEOUT: int = 60
    
    # Security & Limits
    MAX_AUDIO_SIZE_MB: int = 25
    MAX_AUDIO_DURATION_SECONDS: int = 300  # 5 minutes
    MAX_TEXT_LENGTH: int = 10000
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Allowed/Forbidden Operations
    ALLOWED_OPERATIONS: List[str] = [
        "SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "WITH", "UNION"
    ]
    FORBIDDEN_OPERATIONS: List[str] = [
        "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE"
    ]
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 1000
    WS_MESSAGE_MAX_SIZE: int = 1024 * 1024  # 1MB
    
    # Audio Processing
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_FORMAT: str = "wav"
    AUDIO_CHUNK_SIZE: int = 1024
    
    # Model Paths
    MODELS_BASE_PATH: str = "/app/models"
    WHISPER_MODEL_PATH: str = f"{MODELS_BASE_PATH}/whisper"
    COQUI_MODEL_PATH: str = f"{MODELS_BASE_PATH}/coqui"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/whisper_agent.log"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev
        "http://localhost:3000",  # React dev
        "http://localhost:8000",  # Production
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Configurações específicas por serviço
class GatewaySettings(Settings):
    SERVICE_NAME: str = "gateway"
    SERVICE_PORT: int = 8000

class WhisperSettings(Settings):
    SERVICE_NAME: str = "whisper-stt"
    SERVICE_PORT: int = 8001

class CoquiSettings(Settings):
    SERVICE_NAME: str = "coqui-tts"
    SERVICE_PORT: int = 8002

class LLMSettings(Settings):
    SERVICE_NAME: str = "llm-agent"
    SERVICE_PORT: int = 8003

class DatabaseSettings(Settings):
    SERVICE_NAME: str = "database-connector"
    SERVICE_PORT: int = 8004

# Instâncias globais
settings = Settings()
gateway_settings = GatewaySettings()
whisper_settings = WhisperSettings()
coqui_settings = CoquiSettings()
llm_settings = LLMSettings()
database_settings = DatabaseSettings()
```### 2.
 Modelos Compartilhados (backend/shared/models.py)

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums
class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    ERROR = "error"

class LLMProvider(str, Enum):
    OPENROUTER = "openrouter"
    GEMINI = "gemini"
    OPENAI = "openai"

class DatabaseType(str, Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"
    MONGODB = "mongodb"

class MessageType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    SYSTEM = "system"
    ERROR = "error"

# Base Models
class BaseResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: ServiceStatus
    service: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = None

# STT Models
class STTRequest(BaseModel):
    language: Optional[str] = "pt"
    model: Optional[str] = "base"
    temperature: Optional[float] = 0.0
    
class STTResponse(BaseResponse):
    text: str
    confidence: Optional[float] = None
    processing_time: float
    audio_duration: float
    language: str

# TTS Models
class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    speaker_idx: Optional[int] = None
    speed: Optional[float] = 1.0
    language: Optional[str] = "pt"

class TTSResponse(BaseResponse):
    audio_size: int
    processing_time: float
    text_length: int
    voice_used: Optional[str] = None

# LLM Models
class LLMMessage(BaseModel):
    role: str  # user, assistant, system
    content: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class LLMRequest(BaseModel):
    messages: List[LLMMessage]
    provider: Optional[LLMProvider] = LLMProvider.OPENROUTER
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    context: Optional[Dict[str, Any]] = None

class LLMResponse(BaseResponse):
    response: str
    provider: LLMProvider
    model: str
    processing_time: float
    tokens_used: Optional[int] = None

# Database Models
class DatabaseConnection(BaseModel):
    name: str
    type: DatabaseType
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl: Optional[bool] = False
    options: Optional[Dict[str, Any]] = None

class DatabaseQuery(BaseModel):
    connection_name: str
    query: str
    parameters: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = 60

class DatabaseQueryResponse(BaseResponse):
    results: List[Dict[str, Any]]
    columns: List[str]
    row_count: int
    execution_time: float
    query_executed: str

class SchemaInfo(BaseModel):
    database_name: str
    database_type: DatabaseType
    tables: List[Dict[str, Any]]
    total_tables: int

# WebSocket Models
class WebSocketMessage(BaseModel):
    type: MessageType
    data: Dict[str, Any]
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ConversationMessage(BaseModel):
    id: str
    session_id: str
    type: MessageType
    content: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# Gateway Models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    llm_provider: Optional[LLMProvider] = None
    database_connection: Optional[str] = None

class ChatResponse(BaseResponse):
    response: str
    session_id: str
    sql_query: Optional[str] = None
    database_results: Optional[List[Dict[str, Any]]] = None
    audio_url: Optional[str] = None
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None

# Configuration Models
class ServiceConfig(BaseModel):
    service_name: str
    enabled: bool = True
    config: Dict[str, Any]
    health_check_url: str

class SystemConfig(BaseModel):
    services: List[ServiceConfig]
    database_connections: List[DatabaseConnection]
    llm_providers: Dict[str, Dict[str, Any]]
    audio_settings: Dict[str, Any]
```### 3. 
Serviço Whisper STT Otimizado (backend/services/whisper_stt/main.py)

```python
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import whisper
import torch
import tempfile
import os
import logging
import asyncio
from contextlib import asynccontextmanager
import time
from typing import Optional

from backend.shared.config import whisper_settings
from backend.shared.models import STTRequest, STTResponse, HealthResponse, ServiceStatus

# Setup logging
logging.basicConfig(level=whisper_settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

class OptimizedWhisperSTT:
    def __init__(self):
        self.model = None
        self.device = whisper_settings.WHISPER_DEVICE
        self.model_size = whisper_settings.WHISPER_MODEL_SIZE
        self.compute_type = whisper_settings.WHISPER_COMPUTE_TYPE
        
    async def load_model(self):
        """Carrega modelo Whisper otimizado"""
        try:
            logger.info(f"🔄 Carregando Whisper modelo: {self.model_size}")
            
            # Verifica dispositivo disponível
            if self.device == "cuda" and not torch.cuda.is_available():
                logger.warning("CUDA não disponível, usando CPU")
                self.device = "cpu"
            
            # Carrega modelo com otimizações
            self.model = whisper.load_model(
                self.model_size,
                device=self.device,
                download_root=whisper_settings.WHISPER_MODEL_PATH
            )
            
            # Otimizações para CPU
            if self.device == "cpu":
                torch.set_num_threads(4)  # Otimiza threads CPU
            
            logger.info(f"✅ Whisper modelo carregado: {self.model_size} ({self.device})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar modelo Whisper: {e}")
            return False
    
    async def transcribe_audio(self, audio_data: bytes, language: str = "pt") -> Optional[Dict]:
        """Transcreve áudio com otimizações"""
        if not self.model:
            raise HTTPException(status_code=503, detail="Modelo não carregado")
        
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file.flush()
                
                start_time = time.time()
                
                # Transcrição otimizada
                result = self.model.transcribe(
                    temp_file.name,
                    language=language,
                    fp16=False if self.device == "cpu" else True,
                    condition_on_previous_text=False,  # Melhora performance
                    temperature=0.0,  # Mais determinístico
                    compression_ratio_threshold=2.4,
                    logprob_threshold=-1.0,
                    no_speech_threshold=0.6
                )
                
                processing_time = time.time() - start_time
                os.unlink(temp_file.name)
                
                text = result["text"].strip()
                confidence = self._calculate_confidence(result)
                
                logger.info(f"🎤 Transcrição: '{text[:50]}...' ({processing_time:.2f}s)")
                
                return {
                    "text": text,
                    "confidence": confidence,
                    "processing_time": processing_time,
                    "language": result.get("language", language),
                    "segments": len(result.get("segments", []))
                }
                
        except Exception as e:
            logger.error(f"❌ Erro na transcrição: {e}")
            return None
    
    def _calculate_confidence(self, result: dict) -> float:
        """Calcula confiança média baseada nos segmentos"""
        segments = result.get("segments", [])
        if not segments:
            return 0.0
        
        total_confidence = sum(
            segment.get("avg_logprob", -1.0) for segment in segments
        )
        avg_confidence = total_confidence / len(segments)
        
        # Converte logprob para confiança (0-1)
        confidence = max(0.0, min(1.0, (avg_confidence + 1.0)))
        return round(confidence, 3)

# Instância global
whisper_service = OptimizedWhisperSTT()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando Whisper STT Service...")
    
    if await whisper_service.load_model():
        logger.info("✅ Whisper STT Service pronto")
    else:
        logger.error("❌ Falha ao inicializar Whisper STT Service")
    
    yield
    
    logger.info("🔄 Encerrando Whisper STT Service...")

# Criar app FastAPI
app = FastAPI(
    title="Whisper STT Service V2",
    description="Serviço otimizado de Speech-to-Text usando Whisper",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check do serviço"""
    status = ServiceStatus.HEALTHY if whisper_service.model else ServiceStatus.UNHEALTHY
    
    return HealthResponse(
        status=status,
        service=whisper_settings.SERVICE_NAME,
        details={
            "model_loaded": whisper_service.model is not None,
            "device": whisper_service.device,
            "model_size": whisper_service.model_size,
            "compute_type": whisper_service.compute_type
        }
    )

@app.post("/transcribe", response_model=STTResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = "pt",
    model: str = "base"
):
    """Transcreve áudio para texto"""
    try:
        # Validações
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser de áudio")
        
        audio_data = await audio.read()
        size_mb = len(audio_data) / (1024 * 1024)
        
        if size_mb > whisper_settings.MAX_AUDIO_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"Arquivo muito grande. Máximo: {whisper_settings.MAX_AUDIO_SIZE_MB}MB"
            )
        
        # Transcreve
        result = await whisper_service.transcribe_audio(audio_data, language)
        
        if not result:
            raise HTTPException(status_code=400, detail="Falha na transcrição")
        
        return STTResponse(
            success=True,
            message="Transcrição realizada com sucesso",
            text=result["text"],
            confidence=result["confidence"],
            processing_time=result["processing_time"],
            audio_duration=0.0,  # Seria calculado em implementação completa
            language=result["language"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro na transcrição: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.post("/transcribe_batch")
async def transcribe_batch(audios: List[UploadFile] = File(...)):
    """Transcreve múltiplos áudios em lote"""
    results = []
    
    for i, audio in enumerate(audios):
        try:
            audio_data = await audio.read()
            result = await whisper_service.transcribe_audio(audio_data)
            
            if result:
                results.append({
                    "index": i,
                    "filename": audio.filename,
                    "success": True,
                    "text": result["text"],
                    "confidence": result["confidence"],
                    "processing_time": result["processing_time"]
                })
            else:
                results.append({
                    "index": i,
                    "filename": audio.filename,
                    "success": False,
                    "error": "Falha na transcrição"
                })
                
        except Exception as e:
            results.append({
                "index": i,
                "filename": audio.filename,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results, "total": len(audios), "processed": len(results)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=whisper_settings.SERVICE_PORT,
        reload=whisper_settings.DEBUG
    )
```###
 4. Serviço Coqui TTS Avançado (backend/services/coqui_tts/main.py)

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from TTS.api import TTS
import torch
import io
import logging
import tempfile
import os
import asyncio
from contextlib import asynccontextmanager
import time
from typing import Optional, List, Dict

from backend.shared.config import coqui_settings
from backend.shared.models import TTSRequest, TTSResponse, HealthResponse, ServiceStatus

logging.basicConfig(level=coqui_settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

class AdvancedCoquiTTS:
    def __init__(self):
        self.tts = None
        self.model_name = coqui_settings.COQUI_MODEL_NAME
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.available_voices = {}
        self.voice_cache = {}
        
    async def load_model(self):
        """Carrega modelo Coqui TTS com cache de vozes"""
        try:
            logger.info(f"🔄 Carregando Coqui TTS: {self.model_name}")
            
            self.tts = TTS(
                model_name=self.model_name,
                progress_bar=False,
                gpu=self.device == "cuda"
            )
            
            if self.device == "cuda" and torch.cuda.is_available():
                self.tts.to("cuda")
            
            # Carrega informações de vozes disponíveis
            await self._load_voice_info()
            
            logger.info(f"✅ Coqui TTS carregado: {self.model_name} ({self.device})")
            logger.info(f"📢 Vozes disponíveis: {len(self.available_voices)}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar Coqui TTS: {e}")
            return False
    
    async def _load_voice_info(self):
        """Carrega informações sobre vozes disponíveis"""
        try:
            if hasattr(self.tts, 'speakers') and self.tts.speakers:
                for i, speaker in enumerate(self.tts.speakers):
                    self.available_voices[speaker] = {
                        "index": i,
                        "name": speaker,
                        "language": coqui_settings.COQUI_LANGUAGE,
                        "gender": self._detect_gender(speaker),
                        "quality": "high"
                    }
            else:
                # Modelo single-speaker
                self.available_voices["default"] = {
                    "index": 0,
                    "name": "default",
                    "language": coqui_settings.COQUI_LANGUAGE,
                    "gender": "neutral",
                    "quality": "high"
                }
        except Exception as e:
            logger.warning(f"Erro ao carregar info de vozes: {e}")
    
    def _detect_gender(self, speaker_name: str) -> str:
        """Detecta gênero baseado no nome do speaker"""
        male_indicators = ["male", "man", "masculine", "m_"]
        female_indicators = ["female", "woman", "feminine", "f_"]
        
        speaker_lower = speaker_name.lower()
        
        if any(indicator in speaker_lower for indicator in male_indicators):
            return "male"
        elif any(indicator in speaker_lower for indicator in female_indicators):
            return "female"
        else:
            return "neutral"
    
    async def synthesize_speech(
        self, 
        text: str, 
        voice: Optional[str] = None,
        speed: float = 1.0
    ) -> Optional[bytes]:
        """Sintetiza fala com cache e otimizações"""
        if not self.tts:
            raise HTTPException(status_code=503, detail="Modelo TTS não carregado")
        
        try:
            # Cache key
            cache_key = f"{hash(text)}_{voice}_{speed}"
            
            if cache_key in self.voice_cache:
                logger.info(f"🎯 Cache hit para TTS: {text[:30]}...")
                return self.voice_cache[cache_key]
            
            # Determina speaker
            speaker_idx = None
            if voice and voice in self.available_voices:
                speaker_idx = self.available_voices[voice]["index"]
            elif coqui_settings.COQUI_SPEAKER_IDX is not None:
                speaker_idx = coqui_settings.COQUI_SPEAKER_IDX
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                start_time = time.time()
                
                # Síntese com parâmetros otimizados
                if speaker_idx is not None and hasattr(self.tts, 'speakers'):
                    self.tts.tts_to_file(
                        text=text,
                        file_path=temp_file.name,
                        speaker_idx=speaker_idx,
                        speed=speed
                    )
                else:
                    self.tts.tts_to_file(
                        text=text,
                        file_path=temp_file.name,
                        speed=speed
                    )
                
                processing_time = time.time() - start_time
                
                # Lê áudio gerado
                with open(temp_file.name, "rb") as audio_file:
                    audio_data = audio_file.read()
                
                os.unlink(temp_file.name)
                
                # Cache do resultado (limita cache a 100 itens)
                if len(self.voice_cache) < 100:
                    self.voice_cache[cache_key] = audio_data
                
                logger.info(f"🔊 TTS sintetizado: '{text[:50]}...' ({processing_time:.2f}s)")
                return audio_data
                
        except Exception as e:
            logger.error(f"❌ Erro na síntese TTS: {e}")
            return None
    
    def get_available_voices(self) -> Dict[str, Dict]:
        """Retorna vozes disponíveis com metadados"""
        return self.available_voices
    
    def clear_cache(self):
        """Limpa cache de vozes"""
        self.voice_cache.clear()
        logger.info("🧹 Cache de vozes limpo")

# Instância global
coqui_service = AdvancedCoquiTTS()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando Coqui TTS Service...")
    
    if await coqui_service.load_model():
        logger.info("✅ Coqui TTS Service pronto")
    else:
        logger.error("❌ Falha ao inicializar Coqui TTS Service")
    
    yield
    
    logger.info("🔄 Encerrando Coqui TTS Service...")

app = FastAPI(
    title="Coqui TTS Service V2",
    description="Serviço avançado de Text-to-Speech usando Coqui TTS",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check do serviço"""
    status = ServiceStatus.HEALTHY if coqui_service.tts else ServiceStatus.UNHEALTHY
    
    return HealthResponse(
        status=status,
        service=coqui_settings.SERVICE_NAME,
        details={
            "model_loaded": coqui_service.tts is not None,
            "device": coqui_service.device,
            "model_name": coqui_service.model_name,
            "available_voices": len(coqui_service.available_voices),
            "cache_size": len(coqui_service.voice_cache)
        }
    )

@app.get("/voices")
async def get_voices():
    """Lista vozes disponíveis com metadados"""
    voices = coqui_service.get_available_voices()
    
    return {
        "voices": voices,
        "total": len(voices),
        "default_voice": coqui_settings.COQUI_SPEAKER_IDX,
        "supported_languages": [coqui_settings.COQUI_LANGUAGE]
    }

@app.post("/synthesize", response_model=TTSResponse)
async def synthesize_text(request: TTSRequest):
    """Sintetiza texto para áudio"""
    try:
        # Validações
        if len(request.text) > 5000:
            raise HTTPException(
                status_code=400, 
                detail="Texto muito longo (máximo 5000 caracteres)"
            )
        
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Texto não pode estar vazio")
        
        start_time = time.time()
        audio_data = await coqui_service.synthesize_speech(
            text=request.text,
            voice=request.voice,
            speed=request.speed or 1.0
        )
        processing_time = time.time() - start_time
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Falha na síntese de áudio")
        
        return TTSResponse(
            success=True,
            message="Síntese realizada com sucesso",
            audio_size=len(audio_data),
            processing_time=processing_time,
            text_length=len(request.text),
            voice_used=request.voice or "default"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro na síntese: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.post("/synthesize_stream")
async def synthesize_stream(request: TTSRequest):
    """Sintetiza texto e retorna áudio como stream"""
    try:
        audio_data = await coqui_service.synthesize_speech(
            text=request.text,
            voice=request.voice,
            speed=request.speed or 1.0
        )
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Falha na síntese de áudio")
        
        audio_stream = io.BytesIO(audio_data)
        
        return StreamingResponse(
            audio_stream,
            media_type="audio/wav",
            headers={
                "Content-Disposition": f"attachment; filename=tts_output.wav",
                "Content-Length": str(len(audio_data)),
                "X-Processing-Time": str(time.time()),
                "X-Voice-Used": request.voice or "default"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no streaming: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.post("/clear_cache")
async def clear_voice_cache():
    """Limpa cache de vozes"""
    coqui_service.clear_cache()
    return {"message": "Cache limpo com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=coqui_settings.SERVICE_PORT,
        reload=coqui_settings.DEBUG
    )
```### 5. Cone
ctor Universal de Banco de Dados (backend/services/database/main.py)

```python
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, List, Any, Optional
import time
import hashlib

from backend.shared.config import database_settings
from backend.shared.models import (
    DatabaseConnection, DatabaseQuery, DatabaseQueryResponse, 
    SchemaInfo, HealthResponse, ServiceStatus, DatabaseType
)

logging.basicConfig(level=database_settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

class UniversalDatabaseConnector:
    def __init__(self):
        self.engines: Dict[str, Engine] = {}
        self.connections: Dict[str, DatabaseConnection] = {}
        self.query_cache: Dict[str, Any] = {}
        self.schema_cache: Dict[str, SchemaInfo] = {}
        
    async def add_connection(self, connection: DatabaseConnection) -> bool:
        """Adiciona nova conexão de banco de dados"""
        try:
            connection_url = self._build_connection_url(connection)
            
            engine = create_engine(
                connection_url,
                poolclass=QueuePool,
                pool_size=database_settings.MAX_CONNECTIONS_PER_DB,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={"connect_timeout": database_settings.CONNECTION_TIMEOUT}
            )
            
            # Testa conexão
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.engines[connection.name] = engine
            self.connections[connection.name] = connection
            
            logger.info(f"✅ Conexão adicionada: {connection.name} ({connection.type})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao adicionar conexão {connection.name}: {e}")
            return False
    
    def _build_connection_url(self, connection: DatabaseConnection) -> str:
        """Constrói URL de conexão baseada no tipo de banco"""
        if connection.type == DatabaseType.MYSQL:
            return f"mysql+pymysql://{connection.username}:{connection.password}@{connection.host}:{connection.port}/{connection.database}"
        
        elif connection.type == DatabaseType.POSTGRESQL:
            return f"postgresql+psycopg2://{connection.username}:{connection.password}@{connection.host}:{connection.port}/{connection.database}"
        
        elif connection.type == DatabaseType.SQLITE:
            return f"sqlite:///{connection.database}"
        
        elif connection.type == DatabaseType.ORACLE:
            return f"oracle+cx_oracle://{connection.username}:{connection.password}@{connection.host}:{connection.port}/{connection.database}"
        
        elif connection.type == DatabaseType.SQLSERVER:
            return f"mssql+pyodbc://{connection.username}:{connection.password}@{connection.host}:{connection.port}/{connection.database}?driver=ODBC+Driver+17+for+SQL+Server"
        
        else:
            raise ValueError(f"Tipo de banco não suportado: {connection.type}")
    
    async def execute_query(self, query_request: DatabaseQuery) -> DatabaseQueryResponse:
        """Executa query com validação de segurança e cache"""
        if query_request.connection_name not in self.engines:
            raise HTTPException(
                status_code=404, 
                detail=f"Conexão não encontrada: {query_request.connection_name}"
            )
        
        # Validação de segurança
        self._validate_query_security(query_request.query)
        
        # Verifica cache
        cache_key = self._get_cache_key(query_request)
        if cache_key in self.query_cache:
            cached_result = self.query_cache[cache_key]
            logger.info(f"🎯 Cache hit para query: {query_request.query[:50]}...")
            return cached_result
        
        engine = self.engines[query_request.connection_name]
        
        try:
            start_time = time.time()
            
            with engine.connect() as conn:
                result = conn.execute(
                    text(query_request.query), 
                    query_request.parameters or {}
                )
                
                columns = list(result.keys()) if result.keys() else []
                rows = []
                
                for row in result.fetchall():
                    row_dict = {}
                    for i, value in enumerate(row):
                        column_name = columns[i] if i < len(columns) else f"column_{i}"
                        # Converte tipos não serializáveis
                        if hasattr(value, 'isoformat'):  # datetime
                            row_dict[column_name] = value.isoformat()
                        elif isinstance(value, (bytes, bytearray)):
                            row_dict[column_name] = value.decode('utf-8', errors='ignore')
                        else:
                            row_dict[column_name] = value
                    rows.append(row_dict)
                
                execution_time = time.time() - start_time
                
                response = DatabaseQueryResponse(
                    success=True,
                    message="Query executada com sucesso",
                    results=rows,
                    columns=columns,
                    row_count=len(rows),
                    execution_time=execution_time,
                    query_executed=query_request.query
                )
                
                # Cache resultado (limita a 1000 queries)
                if len(self.query_cache) < 1000:
                    self.query_cache[cache_key] = response
                
                logger.info(f"📊 Query executada: {len(rows)} linhas em {execution_time:.2f}s")
                return response
                
        except Exception as e:
            logger.error(f"❌ Erro na execução da query: {e}")
            raise HTTPException(status_code=400, detail=f"Erro na query: {str(e)}")
    
    def _validate_query_security(self, query: str):
        """Valida segurança da query"""
        query_upper = query.upper().strip()
        
        # Verifica operações proibidas
        for forbidden_op in database_settings.FORBIDDEN_OPERATIONS:
            if forbidden_op in query_upper:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Operação proibida: {forbidden_op}"
                )
        
        # Verifica se tem pelo menos uma operação permitida
        if not any(op in query_upper for op in database_settings.ALLOWED_OPERATIONS):
            raise HTTPException(
                status_code=403, 
                detail="Operação não permitida"
            )
    
    def _get_cache_key(self, query_request: DatabaseQuery) -> str:
        """Gera chave de cache para a query"""
        query_str = f"{query_request.connection_name}:{query_request.query}:{query_request.parameters}"
        return hashlib.md5(query_str.encode()).hexdigest()
    
    async def get_schema_info(self, connection_name: str) -> SchemaInfo:
        """Obtém informações do schema com cache"""
        if connection_name not in self.engines:
            raise HTTPException(
                status_code=404, 
                detail=f"Conexão não encontrada: {connection_name}"
            )
        
        # Verifica cache
        if connection_name in self.schema_cache:
            return self.schema_cache[connection_name]
        
        engine = self.engines[connection_name]
        connection_config = self.connections[connection_name]
        
        try:
            inspector = inspect(engine)
            table_names = inspector.get_table_names()
            
            tables_info = []
            for table_name in table_names[:50]:  # Limita a 50 tabelas
                try:
                    columns = inspector.get_columns(table_name)
                    table_info = {
                        "name": table_name,
                        "columns": [
                            {
                                "name": col["name"],
                                "type": str(col["type"]),
                                "nullable": col.get("nullable", True),
                                "default": str(col.get("default")) if col.get("default") else None
                            }
                            for col in columns[:30]  # Limita a 30 colunas por tabela
                        ],
                        "column_count": len(columns)
                    }
                    tables_info.append(table_info)
                except Exception as e:
                    logger.warning(f"Erro ao obter colunas da tabela {table_name}: {e}")
            
            schema_info = SchemaInfo(
                database_name=connection_config.database,
                database_type=connection_config.type,
                tables=tables_info,
                total_tables=len(table_names)
            )
            
            # Cache do schema
            self.schema_cache[connection_name] = schema_info
            
            logger.info(f"📋 Schema obtido: {len(tables_info)} tabelas")
            return schema_info
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter schema: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao obter schema: {str(e)}")
    
    def get_connections(self) -> List[str]:
        """Retorna lista de conexões disponíveis"""
        return list(self.connections.keys())
    
    def clear_cache(self):
        """Limpa todos os caches"""
        self.query_cache.clear()
        self.schema_cache.clear()
        logger.info("🧹 Cache limpo")

# Instância global
db_connector = UniversalDatabaseConnector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando Database Connector Service...")
    
    # Carrega conexões do arquivo de configuração se existir
    # await load_connections_from_config()
    
    logger.info("✅ Database Connector Service pronto")
    yield
    
    logger.info("🔄 Encerrando Database Connector Service...")

app = FastAPI(
    title="Universal Database Connector V2",
    description="Conector universal para múltiplos tipos de banco de dados",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check do serviço"""
    return HealthResponse(
        status=ServiceStatus.HEALTHY,
        service=database_settings.SERVICE_NAME,
        details={
            "active_connections": len(db_connector.engines),
            "cached_queries": len(db_connector.query_cache),
            "cached_schemas": len(db_connector.schema_cache)
        }
    )

@app.post("/connections")
async def add_connection(connection: DatabaseConnection):
    """Adiciona nova conexão de banco de dados"""
    success = await db_connector.add_connection(connection)
    
    if success:
        return {"message": f"Conexão {connection.name} adicionada com sucesso"}
    else:
        raise HTTPException(status_code=400, detail="Falha ao adicionar conexão")

@app.get("/connections")
async def list_connections():
    """Lista conexões disponíveis"""
    connections = db_connector.get_connections()
    return {
        "connections": connections,
        "total": len(connections)
    }

@app.post("/query", response_model=DatabaseQueryResponse)
async def execute_query(query_request: DatabaseQuery):
    """Executa query no banco de dados"""
    return await db_connector.execute_query(query_request)

@app.get("/schema/{connection_name}", response_model=SchemaInfo)
async def get_schema(connection_name: str):
    """Obtém schema do banco de dados"""
    return await db_connector.get_schema_info(connection_name)

@app.post("/clear_cache")
async def clear_cache():
    """Limpa cache de queries e schemas"""
    db_connector.clear_cache()
    return {"message": "Cache limpo com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=database_settings.SERVICE_PORT,
        reload=database_settings.DEBUG
    )
```### 6. Fron
tend Avançado - Interface Principal (frontend/src/components/AudioWeaviteInterface.jsx)

```jsx
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useVoiceAgent } from '../hooks/useVoiceAgent';
import { useAgentModel } from '../hooks/useAgentModel';
import { useDatabaseConnection } from '../hooks/useDatabaseConnection';
import AIModelSelector from './AIModelSelector';
import GeminiVoiceSelector from './GeminiVoiceSelector';
import VoiceConfigPanel from './VoiceConfigPanel';
import ConversationFlow from './ConversationFlow';
import DatabaseConnector from './DatabaseConnector';
import AIStatusRobot from './AIStatusRobot';
import DiagnosticsPanel from './DiagnosticsPanel';

const AudioWeaviteInterface = () => {
    // Estados principais
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [currentMode, setCurrentMode] = useState('voice'); // voice, text, database
    const [showDiagnostics, setShowDiagnostics] = useState(false);
    const [conversation, setConversation] = useState([]);
    const [systemStatus, setSystemStatus] = useState('idle');
    
    // Refs
    const audioRef = useRef(null);
    const conversationRef = useRef(null);
    
    // Hooks customizados
    const {
        startRecording,
        stopRecording,
        isVoiceSupported,
        audioLevel,
        transcription,
        isTranscribing,
        error: voiceError
    } = useVoiceAgent();
    
    const {
        currentModel,
        availableModels,
        switchModel,
        sendMessage,
        isModelReady,
        modelStatus,
        error: modelError
    } = useAgentModel();
    
    const {
        connections,
        activeConnection,
        connectToDatabase,
        executeQuery,
        getSchema,
        connectionStatus,
        error: dbError
    } = useDatabaseConnection();
    
    // Efeitos
    useEffect(() => {
        // Inicialização do componente
        initializeInterface();
        
        return () => {
            // Cleanup
            if (isRecording) {
                handleStopRecording();
            }
        };
    }, []);
    
    useEffect(() => {
        // Auto-scroll da conversa
        if (conversationRef.current) {
            conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
        }
    }, [conversation]);
    
    useEffect(() => {
        // Atualiza status do sistema
        updateSystemStatus();
    }, [isModelReady, connectionStatus, voiceError, modelError, dbError]);
    
    // Funções principais
    const initializeInterface = async () => {
        try {
            setSystemStatus('initializing');
            
            // Verifica suporte a voz
            if (!isVoiceSupported) {
                console.warn('Reconhecimento de voz não suportado neste navegador');
            }
            
            // Carrega configurações salvas
            loadSavedConfiguration();
            
            setSystemStatus('ready');
        } catch (error) {
            console.error('Erro na inicialização:', error);
            setSystemStatus('error');
        }
    };
    
    const loadSavedConfiguration = () => {
        try {
            const savedConfig = localStorage.getItem('audioWeaviteConfig');
            if (savedConfig) {
                const config = JSON.parse(savedConfig);
                // Aplica configurações salvas
                if (config.model) {
                    switchModel(config.model);
                }
                if (config.database) {
                    connectToDatabase(config.database);
                }
            }
        } catch (error) {
            console.error('Erro ao carregar configuração:', error);
        }
    };
    
    const updateSystemStatus = () => {
        if (voiceError || modelError || dbError) {
            setSystemStatus('error');
        } else if (isModelReady && connectionStatus === 'connected') {
            setSystemStatus('ready');
        } else if (isProcessing || isTranscribing) {
            setSystemStatus('processing');
        } else {
            setSystemStatus('idle');
        }
    };
    
    // Handlers de voz
    const handleStartRecording = useCallback(async () => {
        try {
            setIsRecording(true);
            setSystemStatus('listening');
            await startRecording();
        } catch (error) {
            console.error('Erro ao iniciar gravação:', error);
            setIsRecording(false);
            setSystemStatus('error');
        }
    }, [startRecording]);
    
    const handleStopRecording = useCallback(async () => {
        try {
            setIsRecording(false);
            setIsProcessing(true);
            setSystemStatus('processing');
            
            const audioData = await stopRecording();
            
            if (audioData && transcription) {
                await processVoiceInput(transcription, audioData);
            }
        } catch (error) {
            console.error('Erro ao parar gravação:', error);
        } finally {
            setIsProcessing(false);
            setSystemStatus('ready');
        }
    }, [stopRecording, transcription]);
    
    const processVoiceInput = async (text, audioData) => {
        try {
            // Adiciona mensagem do usuário à conversa
            const userMessage = {
                id: Date.now(),
                type: 'user',
                content: text,
                timestamp: new Date(),
                audioData: audioData
            };
            
            setConversation(prev => [...prev, userMessage]);
            
            // Processa com o modelo LLM
            let response;
            
            if (currentMode === 'database' && activeConnection) {
                // Modo banco de dados - gera SQL e executa
                response = await processDatabaseQuery(text);
            } else {
                // Modo conversação normal
                response = await sendMessage(text, conversation);
            }
            
            // Adiciona resposta à conversa
            const assistantMessage = {
                id: Date.now() + 1,
                type: 'assistant',
                content: response.text,
                timestamp: new Date(),
                metadata: response.metadata,
                sqlQuery: response.sqlQuery,
                databaseResults: response.databaseResults
            };
            
            setConversation(prev => [...prev, assistantMessage]);
            
            // Sintetiza resposta em áudio se configurado
            if (response.text) {
                await synthesizeResponse(response.text);
            }
            
        } catch (error) {
            console.error('Erro ao processar entrada de voz:', error);
            
            const errorMessage = {
                id: Date.now(),
                type: 'error',
                content: 'Desculpe, ocorreu um erro ao processar sua mensagem.',
                timestamp: new Date()
            };
            
            setConversation(prev => [...prev, errorMessage]);
        }
    };
    
    const processDatabaseQuery = async (userQuery) => {
        try {
            // Gera SQL usando o modelo LLM
            const schema = await getSchema(activeConnection);
            
            const sqlPrompt = `
                Baseado no schema do banco de dados abaixo, gere uma consulta SQL para: "${userQuery}"
                
                Schema: ${JSON.stringify(schema, null, 2)}
                
                Regras:
                - Use apenas SELECT, SHOW, DESCRIBE
                - Limite resultados com LIMIT
                - Retorne apenas o SQL, sem explicações
            `;
            
            const sqlResponse = await sendMessage(sqlPrompt, []);
            const sqlQuery = extractSQLFromResponse(sqlResponse.text);
            
            if (sqlQuery) {
                // Executa a query
                const results = await executeQuery(activeConnection, sqlQuery);
                
                // Gera resposta em linguagem natural
                const explanationPrompt = `
                    Explique os resultados da consulta SQL de forma clara e amigável:
                    
                    Pergunta original: ${userQuery}
                    SQL executado: ${sqlQuery}
                    Resultados: ${JSON.stringify(results.slice(0, 5), null, 2)}
                    Total de registros: ${results.length}
                `;
                
                const explanation = await sendMessage(explanationPrompt, []);
                
                return {
                    text: explanation.text,
                    sqlQuery: sqlQuery,
                    databaseResults: results,
                    metadata: {
                        queryType: 'database',
                        executionTime: Date.now(),
                        resultCount: results.length
                    }
                };
            } else {
                throw new Error('Não foi possível gerar SQL válido');
            }
            
        } catch (error) {
            console.error('Erro ao processar consulta de banco:', error);
            return {
                text: `Desculpe, não consegui processar sua consulta: ${error.message}`,
                metadata: { error: true }
            };
        }
    };
    
    const extractSQLFromResponse = (response) => {
        // Extrai SQL da resposta do modelo
        const sqlMatch = response.match(/```sql\n(.*?)\n```/s) || 
                         response.match(/```\n(.*?)\n```/s) ||
                         response.match(/(SELECT.*?;?)/is);
        
        return sqlMatch ? sqlMatch[1].trim() : null;
    };
    
    const synthesizeResponse = async (text) => {
        try {
            // Implementa síntese de voz da resposta
            // Conecta com o serviço Coqui TTS
            const response = await fetch('/api/tts/synthesize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            
            if (response.ok) {
                const audioBlob = await response.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                
                if (audioRef.current) {
                    audioRef.current.src = audioUrl;
                    audioRef.current.play();
                }
            }
        } catch (error) {
            console.error('Erro na síntese de voz:', error);
        }
    };
    
    // Handlers de texto
    const handleTextInput = async (text) => {
        if (!text.trim()) return;
        
        setIsProcessing(true);
        await processVoiceInput(text, null);
        setIsProcessing(false);
    };
    
    // Handlers de configuração
    const handleModeChange = (mode) => {
        setCurrentMode(mode);
        
        // Salva configuração
        const config = JSON.parse(localStorage.getItem('audioWeaviteConfig') || '{}');
        config.mode = mode;
        localStorage.setItem('audioWeaviteConfig', JSON.stringify(config));
    };
    
    const handleModelChange = (model) => {
        switchModel(model);
        
        // Salva configuração
        const config = JSON.parse(localStorage.getItem('audioWeaviteConfig') || '{}');
        config.model = model;
        localStorage.setItem('audioWeaviteConfig', JSON.stringify(config));
    };
    
    const handleDatabaseChange = (database) => {
        connectToDatabase(database);
        
        // Salva configuração
        const config = JSON.parse(localStorage.getItem('audioWeaviteConfig') || '{}');
        config.database = database;
        localStorage.setItem('audioWeaviteConfig', JSON.stringify(config));
    };
    
    // Render
    return (
        <div className="audio-weavite-interface">
            {/* Header com status */}
            <div className="interface-header">
                <div className="status-section">
                    <AIStatusRobot status={systemStatus} />
                    <div className="system-info">
                        <span className="model-info">
                            {currentModel?.name || 'Nenhum modelo selecionado'}
                        </span>
                        <span className="connection-info">
                            {activeConnection || 'Sem conexão DB'}
                        </span>
                    </div>
                </div>
                
                <div className="controls-section">
                    <button
                        className={`mode-btn ${currentMode === 'voice' ? 'active' : ''}`}
                        onClick={() => handleModeChange('voice')}
                    >
                        🎤 Voz
                    </button>
                    <button
                        className={`mode-btn ${currentMode === 'text' ? 'active' : ''}`}
                        onClick={() => handleModeChange('text')}
                    >
                        💬 Texto
                    </button>
                    <button
                        className={`mode-btn ${currentMode === 'database' ? 'active' : ''}`}
                        onClick={() => handleModeChange('database')}
                    >
                        🗄️ Banco
                    </button>
                    <button
                        className="diagnostics-btn"
                        onClick={() => setShowDiagnostics(!showDiagnostics)}
                    >
                        🔧 Diagnósticos
                    </button>
                </div>
            </div>
            
            {/* Painel de configuração */}
            <div className="config-panel">
                <AIModelSelector
                    currentModel={currentModel}
                    availableModels={availableModels}
                    onModelChange={handleModelChange}
                    status={modelStatus}
                />
                
                {currentModel?.provider === 'gemini' && (
                    <GeminiVoiceSelector />
                )}
                
                <DatabaseConnector
                    connections={connections}
                    activeConnection={activeConnection}
                    onConnectionChange={handleDatabaseChange}
                    status={connectionStatus}
                />
                
                <VoiceConfigPanel />
            </div>
            
            {/* Área principal */}
            <div className="main-area">
                {/* Conversa */}
                <div className="conversation-area" ref={conversationRef}>
                    <ConversationFlow
                        conversation={conversation}
                        isProcessing={isProcessing}
                        currentMode={currentMode}
                    />
                </div>
                
                {/* Controles de entrada */}
                <div className="input-controls">
                    {currentMode === 'voice' && (
                        <div className="voice-controls">
                            <button
                                className={`record-btn ${isRecording ? 'recording' : ''}`}
                                onClick={isRecording ? handleStopRecording : handleStartRecording}
                                disabled={!isVoiceSupported || isProcessing}
                            >
                                {isRecording ? '⏹️ Parar' : '🎤 Gravar'}
                            </button>
                            
                            {isRecording && (
                                <div className="audio-level">
                                    <div 
                                        className="level-bar"
                                        style={{ width: `${audioLevel * 100}%` }}
                                    />
                                </div>
                            )}
                            
                            {transcription && (
                                <div className="transcription-preview">
                                    {transcription}
                                </div>
                            )}
                        </div>
                    )}
                    
                    {currentMode === 'text' && (
                        <div className="text-controls">
                            <input
                                type="text"
                                placeholder="Digite sua mensagem..."
                                onKeyPress={(e) => {
                                    if (e.key === 'Enter') {
                                        handleTextInput(e.target.value);
                                        e.target.value = '';
                                    }
                                }}
                                disabled={isProcessing}
                            />
                            <button
                                onClick={(e) => {
                                    const input = e.target.previousElementSibling;
                                    handleTextInput(input.value);
                                    input.value = '';
                                }}
                                disabled={isProcessing}
                            >
                                Enviar
                            </button>
                        </div>
                    )}
                    
                    {currentMode === 'database' && (
                        <div className="database-controls">
                            <input
                                type="text"
                                placeholder="Faça uma pergunta sobre os dados..."
                                onKeyPress={(e) => {
                                    if (e.key === 'Enter') {
                                        handleTextInput(e.target.value);
                                        e.target.value = '';
                                    }
                                }}
                                disabled={isProcessing || !activeConnection}
                            />
                            <button
                                onClick={(e) => {
                                    const input = e.target.previousElementSibling;
                                    handleTextInput(input.value);
                                    input.value = '';
                                }}
                                disabled={isProcessing || !activeConnection}
                            >
                                Consultar
                            </button>
                        </div>
                    )}
                </div>
            </div>
            
            {/* Painel de diagnósticos */}
            {showDiagnostics && (
                <DiagnosticsPanel
                    onClose={() => setShowDiagnostics(false)}
                    systemStatus={systemStatus}
                    voiceError={voiceError}
                    modelError={modelError}
                    dbError={dbError}
                />
            )}
            
            {/* Áudio para reprodução */}
            <audio ref={audioRef} style={{ display: 'none' }} />
            
            {/* Indicadores de status */}
            {isTranscribing && (
                <div className="status-overlay">
                    <div className="status-message">
                        🎤 Transcrevendo áudio...
                    </div>
                </div>
            )}
            
            {isProcessing && (
                <div className="status-overlay">
                    <div className="status-message">
                        🤖 Processando com IA...
                    </div>
                </div>
            )}
        </div>
    );
};

export default AudioWeaviteInterface;
```### 7.
 Hook de Conexão com Banco de Dados (frontend/src/hooks/useDatabaseConnection.js)

```javascript
import { useState, useEffect, useCallback } from 'react';

export const useDatabaseConnection = () => {
    const [connections, setConnections] = useState([]);
    const [activeConnection, setActiveConnection] = useState(null);
    const [connectionStatus, setConnectionStatus] = useState('disconnected');
    const [schema, setSchema] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    // Carrega conexões disponíveis
    const loadConnections = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await fetch('/api/database/connections');
            
            if (!response.ok) {
                throw new Error('Falha ao carregar conexões');
            }
            
            const data = await response.json();
            setConnections(data.connections || []);
            
        } catch (err) {
            console.error('Erro ao carregar conexões:', err);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Conecta a um banco de dados
    const connectToDatabase = useCallback(async (connectionName) => {
        try {
            setIsLoading(true);
            setConnectionStatus('connecting');
            setError(null);
            
            // Testa a conexão
            const response = await fetch(`/api/database/test/${connectionName}`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error('Falha na conexão com o banco de dados');
            }
            
            setActiveConnection(connectionName);
            setConnectionStatus('connected');
            
            // Carrega schema automaticamente
            await loadSchema(connectionName);
            
        } catch (err) {
            console.error('Erro na conexão:', err);
            setError(err.message);
            setConnectionStatus('error');
            setActiveConnection(null);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Desconecta do banco atual
    const disconnect = useCallback(() => {
        setActiveConnection(null);
        setConnectionStatus('disconnected');
        setSchema(null);
        setError(null);
    }, []);

    // Carrega schema do banco
    const loadSchema = useCallback(async (connectionName) => {
        try {
            const response = await fetch(`/api/database/schema/${connectionName}`);
            
            if (!response.ok) {
                throw new Error('Falha ao carregar schema');
            }
            
            const schemaData = await response.json();
            setSchema(schemaData);
            
        } catch (err) {
            console.error('Erro ao carregar schema:', err);
            // Não define como erro crítico, apenas log
        }
    }, []);

    // Executa query no banco
    const executeQuery = useCallback(async (connectionName, query, parameters = null) => {
        try {
            setIsLoading(true);
            setError(null);
            
            const response = await fetch('/api/database/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    connection_name: connectionName,
                    query: query,
                    parameters: parameters
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro na execução da query');
            }
            
            const result = await response.json();
            return result.results;
            
        } catch (err) {
            console.error('Erro na execução da query:', err);
            setError(err.message);
            throw err;
        } finally {
            setIsLoading(false);
        }
    }, []);

    // Adiciona nova conexão
    const addConnection = useCallback(async (connectionData) => {
        try {
            setIsLoading(true);
            setError(null);
            
            const response = await fetch('/api/database/connections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(connectionData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Falha ao adicionar conexão');
            }
            
            // Recarrega lista de conexões
            await loadConnections();
            
            return true;
            
        } catch (err) {
            console.error('Erro ao adicionar conexão:', err);
            setError(err.message);
            return false;
        } finally {
            setIsLoading(false);
        }
    }, [loadConnections]);

    // Obtém schema (com cache)
    const getSchema = useCallback(async (connectionName) => {
        if (schema && activeConnection === connectionName) {
            return schema;
        }
        
        await loadSchema(connectionName);
        return schema;
    }, [schema, activeConnection, loadSchema]);

    // Valida query antes da execução
    const validateQuery = useCallback((query) => {
        const queryUpper = query.toUpperCase().trim();
        
        // Operações proibidas
        const forbiddenOps = ['DELETE', 'DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE'];
        const allowedOps = ['SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN', 'WITH'];
        
        // Verifica operações proibidas
        for (const op of forbiddenOps) {
            if (queryUpper.includes(op)) {
                return {
                    valid: false,
                    error: `Operação proibida: ${op}`
                };
            }
        }
        
        // Verifica se tem operação permitida
        const hasAllowedOp = allowedOps.some(op => queryUpper.includes(op));
        if (!hasAllowedOp) {
            return {
                valid: false,
                error: 'Query deve conter uma operação permitida (SELECT, SHOW, etc.)'
            };
        }
        
        return { valid: true };
    }, []);

    // Gera sugestões de query baseadas no schema
    const generateQuerySuggestions = useCallback((userInput) => {
        if (!schema || !schema.tables) {
            return [];
        }
        
        const suggestions = [];
        const inputLower = userInput.toLowerCase();
        
        // Sugestões baseadas em tabelas
        schema.tables.forEach(table => {
            if (table.name.toLowerCase().includes(inputLower)) {
                suggestions.push({
                    type: 'table',
                    query: `SELECT * FROM ${table.name} LIMIT 10`,
                    description: `Mostrar dados da tabela ${table.name}`
                });
            }
            
            // Sugestões baseadas em colunas
            table.columns.forEach(column => {
                if (column.name.toLowerCase().includes(inputLower)) {
                    suggestions.push({
                        type: 'column',
                        query: `SELECT ${column.name} FROM ${table.name} LIMIT 10`,
                        description: `Mostrar coluna ${column.name} da tabela ${table.name}`
                    });
                }
            });
        });
        
        return suggestions.slice(0, 5); // Limita a 5 sugestões
    }, [schema]);

    // Efeito para carregar conexões na inicialização
    useEffect(() => {
        loadConnections();
    }, [loadConnections]);

    // Efeito para salvar conexão ativa no localStorage
    useEffect(() => {
        if (activeConnection) {
            localStorage.setItem('lastDatabaseConnection', activeConnection);
        }
    }, [activeConnection]);

    // Efeito para restaurar última conexão
    useEffect(() => {
        const lastConnection = localStorage.getItem('lastDatabaseConnection');
        if (lastConnection && connections.includes(lastConnection)) {
            connectToDatabase(lastConnection);
        }
    }, [connections, connectToDatabase]);

    return {
        // Estados
        connections,
        activeConnection,
        connectionStatus,
        schema,
        error,
        isLoading,
        
        // Funções
        connectToDatabase,
        disconnect,
        executeQuery,
        addConnection,
        getSchema,
        loadConnections,
        validateQuery,
        generateQuerySuggestions,
        
        // Utilitários
        isConnected: connectionStatus === 'connected',
        hasSchema: !!schema,
        tableCount: schema?.tables?.length || 0
    };
};
```### 8. 
Componente de Conexão com Banco (frontend/src/components/DatabaseConnector.jsx)

```jsx
import React, { useState, useEffect } from 'react';
import { useDatabaseConnection } from '../hooks/useDatabaseConnection';

const DatabaseConnector = ({ connections, activeConnection, onConnectionChange, status }) => {
    const [showAddForm, setShowAddForm] = useState(false);
    const [newConnection, setNewConnection] = useState({
        name: '',
        type: 'mysql',
        host: '',
        port: '',
        database: '',
        username: '',
        password: '',
        ssl: false
    });
    const [testingConnection, setTestingConnection] = useState(false);
    const [showSchema, setShowSchema] = useState(false);
    
    const {
        addConnection,
        getSchema,
        schema,
        validateQuery,
        generateQuerySuggestions,
        isLoading
    } = useDatabaseConnection();

    // Tipos de banco suportados
    const databaseTypes = [
        { value: 'mysql', label: 'MySQL', defaultPort: 3306 },
        { value: 'postgresql', label: 'PostgreSQL', defaultPort: 5432 },
        { value: 'sqlite', label: 'SQLite', defaultPort: null },
        { value: 'oracle', label: 'Oracle', defaultPort: 1521 },
        { value: 'sqlserver', label: 'SQL Server', defaultPort: 1433 }
    ];

    // Atualiza porta padrão quando tipo muda
    useEffect(() => {
        const dbType = databaseTypes.find(type => type.value === newConnection.type);
        if (dbType && dbType.defaultPort) {
            setNewConnection(prev => ({
                ...prev,
                port: dbType.defaultPort.toString()
            }));
        }
    }, [newConnection.type]);

    const handleAddConnection = async (e) => {
        e.preventDefault();
        
        if (!newConnection.name || !newConnection.host) {
            alert('Nome e host são obrigatórios');
            return;
        }
        
        setTestingConnection(true);
        
        try {
            const success = await addConnection({
                ...newConnection,
                port: parseInt(newConnection.port) || null
            });
            
            if (success) {
                setShowAddForm(false);
                setNewConnection({
                    name: '',
                    type: 'mysql',
                    host: '',
                    port: '',
                    database: '',
                    username: '',
                    password: '',
                    ssl: false
                });
                alert('Conexão adicionada com sucesso!');
            }
        } catch (error) {
            alert(`Erro ao adicionar conexão: ${error.message}`);
        } finally {
            setTestingConnection(false);
        }
    };

    const handleShowSchema = async () => {
        if (!activeConnection) return;
        
        try {
            await getSchema(activeConnection);
            setShowSchema(true);
        } catch (error) {
            alert(`Erro ao carregar schema: ${error.message}`);
        }
    };

    const getStatusIcon = () => {
        switch (status) {
            case 'connected': return '🟢';
            case 'connecting': return '🟡';
            case 'error': return '🔴';
            default: return '⚪';
        }
    };

    const getStatusText = () => {
        switch (status) {
            case 'connected': return 'Conectado';
            case 'connecting': return 'Conectando...';
            case 'error': return 'Erro na conexão';
            default: return 'Desconectado';
        }
    };

    return (
        <div className="database-connector">
            <div className="connector-header">
                <h3>🗄️ Conexão com Banco de Dados</h3>
                <div className="status-indicator">
                    {getStatusIcon()} {getStatusText()}
                </div>
            </div>

            <div className="connection-selector">
                <select
                    value={activeConnection || ''}
                    onChange={(e) => onConnectionChange(e.target.value)}
                    disabled={isLoading}
                >
                    <option value="">Selecione uma conexão</option>
                    {connections.map(conn => (
                        <option key={conn} value={conn}>
                            {conn}
                        </option>
                    ))}
                </select>
                
                <button
                    className="add-connection-btn"
                    onClick={() => setShowAddForm(true)}
                    disabled={isLoading}
                >
                    ➕ Adicionar
                </button>
                
                {activeConnection && (
                    <button
                        className="schema-btn"
                        onClick={handleShowSchema}
                        disabled={isLoading}
                    >
                        📋 Schema
                    </button>
                )}
            </div>

            {/* Formulário para adicionar conexão */}
            {showAddForm && (
                <div className="add-connection-modal">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h4>Adicionar Nova Conexão</h4>
                            <button
                                className="close-btn"
                                onClick={() => setShowAddForm(false)}
                            >
                                ✕
                            </button>
                        </div>
                        
                        <form onSubmit={handleAddConnection}>
                            <div className="form-group">
                                <label>Nome da Conexão:</label>
                                <input
                                    type="text"
                                    value={newConnection.name}
                                    onChange={(e) => setNewConnection(prev => ({
                                        ...prev,
                                        name: e.target.value
                                    }))}
                                    placeholder="Ex: Banco Produção"
                                    required
                                />
                            </div>
                            
                            <div className="form-group">
                                <label>Tipo de Banco:</label>
                                <select
                                    value={newConnection.type}
                                    onChange={(e) => setNewConnection(prev => ({
                                        ...prev,
                                        type: e.target.value
                                    }))}
                                >
                                    {databaseTypes.map(type => (
                                        <option key={type.value} value={type.value}>
                                            {type.label}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            
                            <div className="form-row">
                                <div className="form-group">
                                    <label>Host:</label>
                                    <input
                                        type="text"
                                        value={newConnection.host}
                                        onChange={(e) => setNewConnection(prev => ({
                                            ...prev,
                                            host: e.target.value
                                        }))}
                                        placeholder="localhost"
                                        required
                                    />
                                </div>
                                
                                <div className="form-group">
                                    <label>Porta:</label>
                                    <input
                                        type="number"
                                        value={newConnection.port}
                                        onChange={(e) => setNewConnection(prev => ({
                                            ...prev,
                                            port: e.target.value
                                        }))}
                                        placeholder="3306"
                                    />
                                </div>
                            </div>
                            
                            <div className="form-group">
                                <label>Banco de Dados:</label>
                                <input
                                    type="text"
                                    value={newConnection.database}
                                    onChange={(e) => setNewConnection(prev => ({
                                        ...prev,
                                        database: e.target.value
                                    }))}
                                    placeholder="nome_do_banco"
                                />
                            </div>
                            
                            <div className="form-row">
                                <div className="form-group">
                                    <label>Usuário:</label>
                                    <input
                                        type="text"
                                        value={newConnection.username}
                                        onChange={(e) => setNewConnection(prev => ({
                                            ...prev,
                                            username: e.target.value
                                        }))}
                                        placeholder="usuario"
                                    />
                                </div>
                                
                                <div className="form-group">
                                    <label>Senha:</label>
                                    <input
                                        type="password"
                                        value={newConnection.password}
                                        onChange={(e) => setNewConnection(prev => ({
                                            ...prev,
                                            password: e.target.value
                                        }))}
                                        placeholder="senha"
                                    />
                                </div>
                            </div>
                            
                            <div className="form-group">
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={newConnection.ssl}
                                        onChange={(e) => setNewConnection(prev => ({
                                            ...prev,
                                            ssl: e.target.checked
                                        }))}
                                    />
                                    Usar SSL
                                </label>
                            </div>
                            
                            <div className="form-actions">
                                <button
                                    type="button"
                                    onClick={() => setShowAddForm(false)}
                                    disabled={testingConnection}
                                >
                                    Cancelar
                                </button>
                                <button
                                    type="submit"
                                    disabled={testingConnection}
                                >
                                    {testingConnection ? 'Testando...' : 'Adicionar'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Modal do Schema */}
            {showSchema && schema && (
                <div className="schema-modal">
                    <div className="modal-content large">
                        <div className="modal-header">
                            <h4>Schema do Banco: {activeConnection}</h4>
                            <button
                                className="close-btn"
                                onClick={() => setShowSchema(false)}
                            >
                                ✕
                            </button>
                        </div>
                        
                        <div className="schema-content">
                            <div className="schema-summary">
                                <p>
                                    <strong>Banco:</strong> {schema.database_name} 
                                    ({schema.database_type})
                                </p>
                                <p>
                                    <strong>Total de Tabelas:</strong> {schema.total_tables}
                                </p>
                            </div>
                            
                            <div className="tables-list">
                                {schema.tables.map(table => (
                                    <div key={table.name} className="table-item">
                                        <div className="table-header">
                                            <h5>📋 {table.name}</h5>
                                            <span className="column-count">
                                                {table.columns.length} colunas
                                            </span>
                                        </div>
                                        
                                        <div className="columns-list">
                                            {table.columns.map(column => (
                                                <div key={column.name} className="column-item">
                                                    <span className="column-name">
                                                        {column.name}
                                                    </span>
                                                    <span className="column-type">
                                                        {column.type}
                                                    </span>
                                                    {!column.nullable && (
                                                        <span className="not-null">NOT NULL</span>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Informações da conexão ativa */}
            {activeConnection && status === 'connected' && (
                <div className="connection-info">
                    <div className="info-item">
                        <span className="label">Conexão Ativa:</span>
                        <span className="value">{activeConnection}</span>
                    </div>
                    
                    {schema && (
                        <div className="info-item">
                            <span className="label">Tabelas:</span>
                            <span className="value">{schema.total_tables}</span>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default DatabaseConnector;
```### 9. 
Docker Compose Completo (docker/docker-compose.yml)

```yaml
version: '3.8'

services:
  # Frontend (React/Vite)
  frontend:
    build:
      context: ../frontend
      dockerfile: ../docker/frontend.Dockerfile
    container_name: whisper-agent-frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    volumes:
      - ../frontend:/app
      - /app/node_modules
    depends_on:
      - gateway
    restart: unless-stopped

  # Gateway API
  gateway:
    build:
      context: ../backend
      dockerfile: ../docker/gateway.Dockerfile
    container_name: whisper-agent-gateway
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - GATEWAY_HOST=0.0.0.0
      - GATEWAY_PORT=8000
      - WHISPER_SERVICE_URL=http://whisper-stt:8001
      - COQUI_SERVICE_URL=http://coqui-tts:8002
      - LLM_SERVICE_URL=http://llm-agent:8003
      - DATABASE_SERVICE_URL=http://database-connector:8004
    env_file:
      - ../.env
    volumes:
      - ../logs:/app/logs
    depends_on:
      - whisper-stt
      - coqui-tts
      - llm-agent
      - database-connector
    restart: unless-stopped

  # Whisper STT Service
  whisper-stt:
    build:
      context: ../backend
      dockerfile: ../docker/whisper.Dockerfile
    container_name: whisper-agent-stt
    ports:
      - "8001:8001"
    environment:
      - SERVICE_NAME=whisper-stt
      - SERVICE_PORT=8001
      - WHISPER_MODEL_SIZE=base
      - WHISPER_DEVICE=cpu
      - WHISPER_LANGUAGE=pt
    volumes:
      - ../models/whisper:/app/models/whisper
      - ../logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
    restart: unless-stopped

  # Coqui TTS Service
  coqui-tts:
    build:
      context: ../backend
      dockerfile: ../docker/coqui.Dockerfile
    container_name: whisper-agent-tts
    ports:
      - "8002:8002"
    environment:
      - SERVICE_NAME=coqui-tts
      - SERVICE_PORT=8002
      - COQUI_MODEL_NAME=tts_models/pt/cv/vits
      - COQUI_LANGUAGE=pt
    volumes:
      - ../models/coqui:/app/models/coqui
      - ../logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 3G
        reservations:
          memory: 2G
    restart: unless-stopped

  # LLM Agent Service
  llm-agent:
    build:
      context: ../backend
      dockerfile: ../docker/llm.Dockerfile
    container_name: whisper-agent-llm
    ports:
      - "8003:8003"
    environment:
      - SERVICE_NAME=llm-agent
      - SERVICE_PORT=8003
      - DEFAULT_LLM_PROVIDER=openrouter
    env_file:
      - ../.env
    volumes:
      - ../logs:/app/logs
    restart: unless-stopped

  # Database Connector Service
  database-connector:
    build:
      context: ../backend
      dockerfile: ../docker/database.Dockerfile
    container_name: whisper-agent-db
    ports:
      - "8004:8004"
    environment:
      - SERVICE_NAME=database-connector
      - SERVICE_PORT=8004
    volumes:
      - ../logs:/app/logs
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: whisper-agent-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - ../ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - gateway
    restart: unless-stopped

  # Redis (para cache e sessões)
  redis:
    image: redis:7-alpine
    container_name: whisper-agent-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  # PostgreSQL (banco de exemplo/configuração)
  postgres:
    image: postgres:15-alpine
    container_name: whisper-agent-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: whisper_agent
      POSTGRES_USER: whisper_user
      POSTGRES_PASSWORD: whisper_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ../sql/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped

  # Monitoring - Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: whisper-agent-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ../monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    restart: unless-stopped

  # Monitoring - Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: whisper-agent-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
      - ../monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ../monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
  prometheus_data:
  grafana_data:

networks:
  default:
    name: whisper-agent-network
    driver: bridge
```### 10
. Script de Setup Automatizado (scripts/setup.sh)

```bash
#!/bin/bash

set -e  # Exit on any error

echo "🚀 Configurando Whisper Agent BD V2 - Sistema Híbrido..."
echo "================================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências do sistema..."
    
    # Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker não encontrado. Instale o Docker primeiro."
        exit 1
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose não encontrado. Instale o Docker Compose primeiro."
        exit 1
    fi
    
    # Node.js (para frontend)
    if ! command -v node &> /dev/null; then
        log_error "Node.js não encontrado. Instale o Node.js primeiro."
        exit 1
    fi
    
    # Python (para backend)
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 não encontrado. Instale o Python 3 primeiro."
        exit 1
    fi
    
    log_success "Todas as dependências estão instaladas"
}

# Criar estrutura de diretórios
create_directories() {
    log_info "Criando estrutura de diretórios..."
    
    mkdir -p models/{whisper,coqui,embeddings}
    mkdir -p logs
    mkdir -p ssl
    mkdir -p monitoring/{prometheus,grafana/{dashboards,datasources}}
    mkdir -p sql
    mkdir -p data/{uploads,cache}
    
    log_success "Estrutura de diretórios criada"
}

# Configurar arquivo .env
setup_env_file() {
    log_info "Configurando arquivo .env..."
    
    if [ ! -f .env ]; then
        log_info "Criando arquivo .env a partir do exemplo..."
        cp .env.example .env
        
        # Gerar chaves aleatórias
        SECRET_KEY=$(openssl rand -hex 32)
        JWT_SECRET=$(openssl rand -hex 32)
        
        # Substituir placeholders
        sed -i "s/your_secret_key_here/$SECRET_KEY/g" .env
        sed -i "s/your_jwt_secret_here/$JWT_SECRET/g" .env
        
        log_warning "Arquivo .env criado. Configure suas chaves de API antes de continuar:"
        log_warning "- OPENROUTER_API_KEY"
        log_warning "- GEMINI_API_KEY"
        log_warning "- OPENAI_API_KEY (opcional)"
        
        read -p "Pressione Enter para continuar após configurar as chaves..."
    else
        log_success "Arquivo .env já existe"
    fi
}

# Download de modelos
download_models() {
    log_info "Baixando modelos necessários..."
    
    # Whisper models
    if [ ! -d "models/whisper" ] || [ -z "$(ls -A models/whisper)" ]; then
        log_info "Baixando modelos Whisper..."
        python3 -c "
import whisper
import os
os.makedirs('models/whisper', exist_ok=True)
print('Baixando modelo Whisper base...')
whisper.load_model('base', download_root='./models/whisper')
print('Modelo Whisper baixado com sucesso!')
"
        log_success "Modelos Whisper baixados"
    else
        log_success "Modelos Whisper já existem"
    fi
    
    # Coqui TTS models (serão baixados automaticamente na primeira execução)
    log_info "Modelos Coqui TTS serão baixados automaticamente na primeira execução"
}

# Configurar frontend
setup_frontend() {
    log_info "Configurando frontend..."
    
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        log_info "Instalando dependências do frontend..."
        npm install
    else
        log_info "Atualizando dependências do frontend..."
        npm update
    fi
    
    # Build para produção
    log_info "Fazendo build do frontend..."
    npm run build
    
    cd ..
    log_success "Frontend configurado"
}

# Configurar backend
setup_backend() {
    log_info "Configurando backend..."
    
    # Criar ambientes virtuais para cada serviço
    services=("gateway" "whisper_stt" "coqui_tts" "llm_agent" "database")
    
    for service in "${services[@]}"; do
        service_path="backend/services/$service"
        
        if [ -d "$service_path" ]; then
            log_info "Configurando serviço: $service"
            
            cd "$service_path"
            
            # Criar venv se não existir
            if [ ! -d "venv" ]; then
                python3 -m venv venv
            fi
            
            # Ativar venv e instalar dependências
            source venv/bin/activate
            
            # Instalar dependências específicas do serviço
            if [ -f "../../requirements/${service}.txt" ]; then
                pip install -r "../../requirements/${service}.txt"
            fi
            
            deactivate
            cd - > /dev/null
        fi
    done
    
    log_success "Backend configurado"
}

# Configurar banco de dados
setup_database() {
    log_info "Configurando banco de dados..."
    
    # Criar script SQL de inicialização
    cat > sql/init.sql << 'EOF'
-- Whisper Agent BD V2 - Inicialização do Banco
-- Tabelas para configuração e logs do sistema

CREATE TABLE IF NOT EXISTS system_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS database_connections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    host VARCHAR(255) NOT NULL,
    port INTEGER,
    database_name VARCHAR(255),
    username VARCHAR(255),
    encrypted_password TEXT,
    ssl_enabled BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS conversation_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    user_message TEXT,
    assistant_response TEXT,
    sql_query TEXT,
    execution_time FLOAT,
    model_used VARCHAR(255),
    database_used VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(255) NOT NULL,
    metric_value FLOAT NOT NULL,
    metric_unit VARCHAR(50),
    service_name VARCHAR(255),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir configurações padrão
INSERT INTO system_config (key, value, description) VALUES
('default_llm_provider', 'openrouter', 'Provedor LLM padrão'),
('default_whisper_model', 'base', 'Modelo Whisper padrão'),
('default_tts_voice', 'default', 'Voz TTS padrão'),
('max_audio_duration', '300', 'Duração máxima de áudio em segundos'),
('enable_conversation_logging', 'true', 'Habilitar log de conversas')
ON CONFLICT (key) DO NOTHING;

EOF

    log_success "Scripts de banco de dados criados"
}

# Configurar monitoramento
setup_monitoring() {
    log_info "Configurando monitoramento..."
    
    # Prometheus config
    cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'whisper-agent-gateway'
    static_configs:
      - targets: ['gateway:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'whisper-agent-services'
    static_configs:
      - targets: 
        - 'whisper-stt:8001'
        - 'coqui-tts:8002'
        - 'llm-agent:8003'
        - 'database-connector:8004'
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF

    # Grafana datasource
    mkdir -p monitoring/grafana/datasources
    cat > monitoring/grafana/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

    log_success "Monitoramento configurado"
}

# Build das imagens Docker
build_docker_images() {
    log_info "Construindo imagens Docker..."
    
    # Build das imagens
    docker-compose -f docker/docker-compose.yml build --parallel
    
    log_success "Imagens Docker construídas"
}

# Verificar saúde dos serviços
check_services_health() {
    log_info "Verificando saúde dos serviços..."
    
    services=("gateway:8000" "whisper-stt:8001" "coqui-tts:8002" "llm-agent:8003" "database-connector:8004")
    
    for service in "${services[@]}"; do
        service_name=$(echo $service | cut -d':' -f1)
        port=$(echo $service | cut -d':' -f2)
        
        log_info "Verificando $service_name..."
        
        # Aguardar até 60 segundos para o serviço ficar disponível
        for i in {1..12}; do
            if curl -s -f "http://localhost:$port/health" > /dev/null; then
                log_success "$service_name está saudável"
                break
            else
                if [ $i -eq 12 ]; then
                    log_warning "$service_name não está respondendo"
                else
                    sleep 5
                fi
            fi
        done
    done
}

# Função principal
main() {
    echo "Iniciando setup do Whisper Agent BD V2..."
    echo "Este processo pode levar alguns minutos..."
    echo ""
    
    check_dependencies
    create_directories
    setup_env_file
    download_models
    setup_frontend
    setup_backend
    setup_database
    setup_monitoring
    build_docker_images
    
    log_success "Setup concluído com sucesso!"
    echo ""
    echo "================================================================"
    echo "🎉 Whisper Agent BD V2 está pronto para uso!"
    echo ""
    echo "Para iniciar o sistema:"
    echo "  docker-compose -f docker/docker-compose.yml up -d"
    echo ""
    echo "Para acessar:"
    echo "  Frontend: http://localhost:3000"
    echo "  API Gateway: http://localhost:8000"
    echo "  Grafana: http://localhost:3001 (admin/admin123)"
    echo ""
    echo "Para monitorar logs:"
    echo "  docker-compose -f docker/docker-compose.yml logs -f"
    echo ""
    echo "Para parar o sistema:"
    echo "  docker-compose -f docker/docker-compose.yml down"
    echo "================================================================"
}

# Executar função principal
main "$@"
```### 1
1. Arquivo .env.example Completo

```env
# Environment Configuration
ENVIRONMENT=development
DEBUG=true

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here

# Services Configuration
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8000
FRONTEND_URL=http://localhost:3000

# Internal Services URLs (Docker Network)
WHISPER_SERVICE_URL=http://whisper-stt:8001
COQUI_SERVICE_URL=http://coqui-tts:8002
LLM_SERVICE_URL=http://llm-agent:8003
DATABASE_SERVICE_URL=http://database-connector:8004

# Whisper STT Configuration
WHISPER_MODEL_SIZE=base
WHISPER_LANGUAGE=pt
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8

# Coqui TTS Configuration
COQUI_MODEL_NAME=tts_models/pt/cv/vits
COQUI_LANGUAGE=pt
COQUI_SPEAKER_IDX=0

# LLM Configuration
DEFAULT_LLM_PROVIDER=openrouter

# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_DEFAULT_MODEL=deepseek/deepseek-chat

# Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
GEMINI_DEFAULT_MODEL=gemini-1.5-flash

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_DEFAULT_MODEL=gpt-3.5-turbo

# Database Configuration (System Database)
DATABASE_URL=postgresql://whisper_user:whisper_pass@postgres:5432/whisper_agent

# External Database Connections (Examples)
# MYSQL_EXAMPLE_HOST=localhost
# MYSQL_EXAMPLE_PORT=3306
# MYSQL_EXAMPLE_USER=root
# MYSQL_EXAMPLE_PASSWORD=password
# MYSQL_EXAMPLE_DATABASE=example_db

# POSTGRES_EXAMPLE_HOST=localhost
# POSTGRES_EXAMPLE_PORT=5432
# POSTGRES_EXAMPLE_USER=postgres
# POSTGRES_EXAMPLE_PASSWORD=password
# POSTGRES_EXAMPLE_DATABASE=example_db

# Security & Limits
MAX_AUDIO_SIZE_MB=25
MAX_AUDIO_DURATION_SECONDS=300
MAX_TEXT_LENGTH=10000
RATE_LIMIT_PER_MINUTE=100

# WebSocket Configuration
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=1000
WS_MESSAGE_MAX_SIZE=1048576

# Audio Processing
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1
AUDIO_FORMAT=wav
AUDIO_CHUNK_SIZE=1024

# Model Paths
MODELS_BASE_PATH=/app/models
WHISPER_MODEL_PATH=/app/models/whisper
COQUI_MODEL_PATH=/app/models/coqui

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=logs/whisper_agent.log

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8000

# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true

# File Upload
UPLOAD_MAX_SIZE=100MB
UPLOAD_ALLOWED_TYPES=audio/wav,audio/mp3,audio/ogg,application/pdf,text/plain

# Cache Configuration
CACHE_TTL=3600
CACHE_MAX_SIZE=1000

# Session Configuration
SESSION_TIMEOUT=1800
SESSION_CLEANUP_INTERVAL=300

# Feature Flags
ENABLE_CONVERSATION_LOGGING=true
ENABLE_AUDIO_CACHE=true
ENABLE_QUERY_CACHE=true
ENABLE_SCHEMA_CACHE=true
ENABLE_VOICE_SYNTHESIS=true
ENABLE_PDF_PROCESSING=true
ENABLE_BATCH_PROCESSING=true

# Development Configuration
DEV_RELOAD=true
DEV_DEBUG_SQL=false
DEV_MOCK_SERVICES=false
```

## Como Usar o Sistema Híbrido

### 1. Setup Inicial Automatizado
```bash
# Clone o projeto
git clone <repo> whisper_agent_bd_v2
cd whisper_agent_bd_v2

# Execute o setup automatizado
chmod +x scripts/setup.sh
./scripts/setup.sh

# Configure suas chaves de API no arquivo .env
nano .env
```

### 2. Iniciar Sistema Completo
```bash
# Desenvolvimento (com hot reload)
docker-compose -f docker/docker-compose.yml -f docker-compose.dev.yml up --build

# Produção
docker-compose -f docker/docker-compose.yml up -d --build
```

### 3. Testar com Celular
1. **Encontre o IP do servidor**: `ip addr show` (Linux) ou `ipconfig` (Windows)
2. **Acesse no celular**: `http://IP_DO_SERVIDOR:3000`
3. **Configure conexão com banco** na interface
4. **Teste funcionalidades**:
   - Gravação de áudio com transcrição
   - Chat de texto com IA
   - Consultas ao banco de dados por voz
   - Síntese de voz das respostas

### 4. Monitoramento e Logs
```bash
# Logs de todos os serviços
docker-compose logs -f

# Logs de um serviço específico
docker-compose logs -f whisper-stt

# Métricas no Grafana
# http://localhost:3001 (admin/admin123)

# Status dos serviços
curl http://localhost:8000/api/health
```

## Vantagens da Arquitetura Híbrida V2

### ✅ **Interface Avançada**
- React/Vite com componentes modernos
- Seletor inteligente de modelos LLM
- Configuração visual de vozes TTS
- Painel de diagnósticos em tempo real
- Suporte a PDF com IA

### ✅ **Backend Robusto**
- Whisper FastAPI otimizado para baixa latência
- Coqui TTS com cache inteligente de vozes
- Conector universal para múltiplos bancos
- Agentes LLM multi-provider (OpenRouter/Gemini/OpenAI)
- Sistema de cache avançado

### ✅ **Integração Completa**
- WebSocket para comunicação em tempo real
- Sistema de sessões e contexto
- Validação de segurança para queries SQL
- Logs estruturados e métricas
- Monitoramento com Prometheus/Grafana

### ✅ **Flexibilidade Máxima**
- Conecta com qualquer aplicação existente
- Suporte a MySQL, PostgreSQL, Oracle, SQL Server
- Múltiplos provedores de LLM
- Configuração via interface web
- Deploy escalável com Docker

### ✅ **Experiência do Usuário**
- Interface responsiva mobile-first
- Feedback visual em tempo real
- Suporte offline com Service Worker
- Diagnósticos automáticos
- Configuração persistente

Esta arquitetura híbrida combina o melhor dos dois mundos: uma interface web moderna e intuitiva com um backend robusto e escalável, perfeita para integração com sistemas empresariais existentes!