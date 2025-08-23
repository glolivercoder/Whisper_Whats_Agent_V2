# 🤖 WhatsApp Voice Agent V2 - Desenvolvimento Rápido

## 🚀 Quick Start (5 minutos)

### 1. Executar o Projeto
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh && ./start.sh
```

### 2. Acessar Interface
- **Navegador**: http://localhost:8000
- **Interface de Voz**: Clique no microfone para gravar
- **Chat de Texto**: Digite mensagens na caixa

### 3. Conectar WhatsApp (Opcional)
- Configure webhook: `http://SEU_IP:8000/api/whatsapp/webhook`
- Teste com: `python test_whatsapp.py`

## 📱 Funcionalidades Principais

### ✅ Interface Visual Completa
- 🎤 **Gravação de Voz** - Clique no microfone
- 💬 **Chat de Texto** - Digite ou fale
- 🔊 **TTS On/Off** - Switch para ativar/desativar voz
- 📱 **Design Responsivo** - Funciona no celular

### ✅ Processamento de Áudio
- **STT (Speech-to-Text)** - Whisper OpenAI
- **Transcrição em Tempo Real** - Português BR
- **Feedback Visual** - Status e progresso

### ✅ Integração WhatsApp
- **Webhook Ready** - Recebe mensagens do WhatsApp
- **Respostas Automáticas** - IA processa e responde
- **Suporte Audio/Texto** - Múltiplos formatos

## 🛠️ Tecnologias Usadas

### Backend (FastAPI)
```python
# Principais componentes
- FastAPI (API REST + WebSocket)
- Whisper (STT - Speech to Text)
- WebSocket (Comunicação em tempo real)
- Placeholder TTS (Coqui TTS em desenvolvimento)
```

### Frontend (HTML/JS)
```javascript
// Recursos da interface
- Gravação de áudio nativa
- WebSocket real-time
- Interface responsiva
- Controles de voz/texto
```

## 📋 Estrutura do Projeto

```
whisper_agent_bd_v2/
├── backend/
│   └── main.py              # FastAPI server
├── templates/
│   └── index.html           # Interface web
├── requirements.txt         # Dependências Python
├── start.bat               # Iniciar Windows
├── test_whatsapp.py        # Teste WhatsApp
└── README.md               # Este arquivo
```

## 🔧 Configuração Avançada

### 1. Modelos de IA
```python
# Editar backend/main.py
WHISPER_MODEL = "base"  # tiny, base, small, medium, large
LANGUAGE = "pt"         # Português brasileiro
```

### 2. WhatsApp Business API
```python
# Configure em test_whatsapp.py
PHONE_TOKEN = "seu_token_aqui"
PHONE_NUMBER_ID = "seu_numero_id"
WEBHOOK_URL = "http://seu_ip:8000/api/whatsapp/webhook"
```

### 3. TTS (Text-to-Speech)
```python
# Para implementar Coqui TTS
pip install TTS
# Editar synthesize_speech() em main.py
```

## 📱 Teste no Celular

### 1. Descobrir IP do Servidor
```bash
# Windows
ipconfig

# Linux/Mac  
ifconfig
```

### 2. Acessar do Celular
- Conecte na mesma WiFi
- Acesse: `http://IP_DO_SERVIDOR:8000`
- Teste gravação de voz

### 3. WhatsApp Integration
- Configure webhook no WhatsApp Business
- Teste com `python test_whatsapp.py`

## 🐛 Resolução de Problemas

### Erro de Microfone
- Permitir acesso ao microfone no navegador
- Usar HTTPS em produção

### Erro de Conexão
- Verificar firewall
- Conferir IP e porta
- Testar com `curl http://localhost:8000/health`

### Modelo Whisper não carrega
- Aguardar download inicial (primeira execução)
- Verificar espaço em disco (modelos são grandes)

## 🔄 Próximos Passos

### Fase 1 - Básico (Implementado ✅)
- [x] Interface web funcional
- [x] STT com Whisper
- [x] WebSocket real-time
- [x] Estrutura WhatsApp

### Fase 2 - Avançado (A fazer)
- [ ] Implementar Coqui TTS real
- [ ] Integração LLM (OpenRouter/Gemini)
- [ ] Banco de dados
- [ ] Deploy produção

### Fase 3 - WhatsApp Real
- [ ] WhatsApp Business API oficial
- [ ] Autenticação e sessões
- [ ] Multi-usuário
- [ ] Monitoramento

## 📞 Suporte

- **Logs**: Verificar terminal onde roda o servidor
- **Health Check**: http://localhost:8000/health
- **WebSocket Test**: Usar DevTools do navegador
- **WhatsApp Test**: Executar `python test_whatsapp.py`

---

**🎯 Objetivo**: Interface funcional para teste de voz + WhatsApp em desenvolvimento local

**⏱️ Tempo para rodar**: ~5 minutos

**📱 Compatível**: Desktop, Mobile, WhatsApp (webhook)