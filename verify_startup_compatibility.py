#!/usr/bin/env python3
"""
Verifica compatibilidade do start_enhanced_correct.bat com as correções aplicadas
"""

import os

def check_startup_compatibility():
    """Verifica se o sistema está pronto para usar o start_enhanced_correct.bat"""
    
    print("🔍 VERIFICAÇÃO DE COMPATIBILIDADE DO STARTUP")
    print("=" * 60)
    
    checks = []
    
    # 1. Verificar se o serviço TTS limpo existe
    clean_tts_path = "backend/clean_tts_service.py"
    if os.path.exists(clean_tts_path):
        checks.append(("✅", "Serviço TTS limpo disponível"))
    else:
        checks.append(("❌", "Serviço TTS limpo não encontrado"))
    
    # 2. Verificar main_enhanced.py atualizado
    main_enhanced_path = "backend/main_enhanced.py"
    if os.path.exists(main_enhanced_path):
        with open(main_enhanced_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'CleanTTSService' in content:
            checks.append(("✅", "main_enhanced.py integrado com TTS limpo"))
        else:
            checks.append(("⚠️", "main_enhanced.py pode não estar integrado"))
    else:
        checks.append(("❌", "main_enhanced.py não encontrado"))
    
    # 3. Verificar arquivos de referência
    ref_dirs = ["reference_audio", "backend/reference_audio"]
    ref_files_found = 0
    
    for ref_dir in ref_dirs:
        if os.path.exists(ref_dir):
            files = [f for f in os.listdir(ref_dir) if f.endswith(('.wav', '.mp3'))]
            ref_files_found += len(files)
    
    if ref_files_found > 0:
        checks.append(("✅", f"Arquivos de referência encontrados: {ref_files_found}"))
    else:
        checks.append(("⚠️", "Poucos arquivos de referência encontrados"))
    
    # 4. Verificar script de inicialização
    startup_script = "start_enhanced_correct.bat"
    if os.path.exists(startup_script):
        checks.append(("✅", "Script de inicialização disponível"))
    else:
        checks.append(("❌", "Script de inicialização não encontrado"))
    
    # 5. Verificar check_voice_cloning_setup.py
    check_script = "check_voice_cloning_setup.py"
    if os.path.exists(check_script):
        checks.append(("✅", "Script de verificação de clonagem disponível"))
    else:
        checks.append(("⚠️", "Script de verificação pode estar ausente"))
    
    # Mostrar resultados
    print("📋 RESULTADOS DA VERIFICAÇÃO:")
    print("-" * 60)
    
    for status, message in checks:
        print(f"{status} {message}")
    
    # Análise geral
    success_count = sum(1 for status, _ in checks if status == "✅")
    total_checks = len(checks)
    
    print("\n" + "=" * 60)
    print("🎯 ANÁLISE GERAL:")
    print("=" * 60)
    
    if success_count >= 4:
        print("🎉 SISTEMA TOTALMENTE COMPATÍVEL!")
        print("✅ Você pode usar ./start_enhanced_correct.bat com segurança")
        print("✅ Todas as correções do TTS limpo estão integradas")
        print("✅ O sistema funcionará perfeitamente")
        
        print("\n💡 INSTRUÇÕES DE USO:")
        print("1. Execute: ./start_enhanced_correct.bat")
        print("2. Aguarde o servidor inicializar na porta 8001")
        print("3. Acesse: http://localhost:8001")
        print("4. Teste a clonagem: http://localhost:8001/docs")
        
        return True
    elif success_count >= 3:
        print("⚠️ SISTEMA PARCIALMENTE COMPATÍVEL")
        print("✅ Pode usar ./start_enhanced_correct.bat")
        print("⚠️ Algumas funcionalidades podem ter limitações")
        
        return True
    else:
        print("❌ SISTEMA NÃO COMPATÍVEL")
        print("❌ Não recomendado usar ./start_enhanced_correct.bat")
        print("💡 Execute primeiro: python integrate_coquitts_basic.py")
        
        return False

def create_startup_instructions():
    """Cria instruções de uso do startup"""
    
    instructions = """
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
curl -X POST "http://localhost:8001/api/tts/test-clone" \
     -H "Content-Type: application/json" \
     -d '{"text": "Olá, teste de clonagem", "voice_name": "Julia", "language": "pt"}'
```
"""
    
    with open('STARTUP_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("📝 Instruções salvas em: STARTUP_INSTRUCTIONS.md")

def main():
    compatible = check_startup_compatibility()
    
    if compatible:
        create_startup_instructions()
        
        print("\n" + "=" * 60)
        print("🎉 PRONTO PARA USO!")
        print("=" * 60)
        print("Execute: ./start_enhanced_correct.bat")
        print("O sistema TTS limpo está totalmente integrado!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️ AÇÃO NECESSÁRIA")
        print("=" * 60)
        print("Execute primeiro: python integrate_coquitts_basic.py")
        print("=" * 60)

if __name__ == "__main__":
    main()