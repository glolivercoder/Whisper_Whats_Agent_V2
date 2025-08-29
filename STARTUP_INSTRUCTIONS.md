
# 🚀 INSTRUÇÕES DE INICIALIZAÇÃO

## Usando start_enhanced_correct.bat (RECOMENDADO)

1. **Inicializar o servidor:**
   ```
   ./start_enhanced_correct.bat
   ```

2. **O que o script faz:**
   - ✅ Verifica e ativa o ambiente virtual
   - ✅ Instala dependências se necessário
   - ✅ Configura variáveis de ambiente (COQUI_TOS_AGREED=1)
   - ✅ Limpa portas em uso
   - ✅ Cria diretórios necessários
   - ✅ Inicia servidor na porta 8001

3. **URLs importantes:**
   - 🌐 Interface principal: http://localhost:8001
   - 📖 Documentação API: http://localhost:8001/docs
   - 🔍 Status do sistema: http://localhost:8001/health
   - 🎭 Status TTS: http://localhost:8001/api/tts/status

4. **Endpoints de clonagem:**
   - POST /api/tts/test-clone - Testar voz clonada
   - GET /api/tts/list-cloned-voices - Listar vozes
   - POST /api/tts/clone-voice - Clonar nova voz

## Sistema TTS Limpo Integrado

✅ **Baseado no coquittsbasic funcional**
✅ **XTTS v2 como engine principal**
✅ **Sem erros de encoding Unicode**
✅ **Clonagem de voz estável**
✅ **Arquivos de referência incluídos**

## Solução de Problemas

Se houver problemas:
1. Verifique se Python está instalado
2. Execute como Administrador se necessário
3. Verifique se as portas 8001/8002 estão livres
4. Consulte os logs no terminal

## Teste Rápido

Após inicializar, teste com:
```bash
curl -X POST "http://localhost:8001/api/tts/test-clone"      -H "Content-Type: application/json"      -d '{"text": "Olá, teste de clonagem", "voice_name": "Julia", "language": "pt"}'
```
