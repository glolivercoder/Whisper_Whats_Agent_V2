#!/usr/bin/env python3
"""
Debug das questões de integração - verificar se as correções foram aplicadas corretamente
"""

import os
import subprocess
import time
import threading
import requests
from datetime import datetime

def check_clean_tts_integration():
    """Verifica se o CleanTTSService foi realmente integrado"""
    
    print("🔍 VERIFICANDO INTEGRAÇÃO DO CLEAN TTS SERVICE")
    print("=" * 60)
    
    # 1. Verificar se o arquivo clean_tts_service.py existe
    clean_tts_path = "backend/clean_tts_service.py"
    if os.path.exists(clean_tts_path):
        print("✅ clean_tts_service.py existe")
        
        with open(clean_tts_path, 'r', encoding='utf-8') as f:
            clean_content = f.read()
        
        if 'CleanTTSService' in clean_content:
            print("✅ CleanTTSService definido no arquivo")
        else:
            print("❌ CleanTTSService não encontrado no arquivo")
    else:
        print("❌ clean_tts_service.py NÃO EXISTE!")
        return False
    
    # 2. Verificar integração no main_enhanced.py
    main_path = "backend/main_enhanced.py"
    if os.path.exists(main_path):
        with open(main_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        print("\n📋 VERIFICAÇÕES NO main_enhanced.py:")
        
        # Verificar import
        if 'from clean_tts_service import CleanTTSService' in main_content:
            print("✅ Import do CleanTTSService encontrado")
        else:
            print("❌ Import do CleanTTSService NÃO ENCONTRADO")
        
        # Verificar inicialização
        if 'self.clean_tts = CleanTTSService()' in main_content:
            print("✅ Inicialização do CleanTTSService encontrada")
        else:
            print("❌ Inicialização do CleanTTSService NÃO ENCONTRADA")
        
        # Verificar uso no synthesize_speech
        if 'self.clean_tts.synthesize_speech' in main_content:
            print("✅ Uso do CleanTTSService no synthesize_speech encontrado")
        else:
            print("❌ Uso do CleanTTSService NÃO ENCONTRADO")
        
        return True
    else:
        print("❌ main_enhanced.py não encontrado!")
        return False

def test_server_with_logs():
    """Testa o servidor e captura logs detalhados"""
    
    print("\n🧪 TESTANDO SERVIDOR COM LOGS DETALHADOS")
    print("=" * 60)
    
    # Iniciar servidor
    print("🚀 Iniciando servidor...")
    process = subprocess.Popen(
        ['python', '-m', 'uvicorn', 'main_enhanced:app', '--host', '0.0.0.0', '--port', '8000'],
        cwd='backend',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    logs = []
    server_ready = False
    errors = []
    
    def capture_logs():
        nonlocal server_ready, logs, errors
        while True:
            line = process.stdout.readline()
            if line:
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                log_entry = f"[{timestamp}] {line.strip()}"
                logs.append(log_entry)
                print(log_entry)
                
                # Detectar erros específicos
                if 'ImportError' in line or 'ModuleNotFoundError' in line:
                    errors.append(f"IMPORT ERROR: {line.strip()}")
                elif 'AttributeError' in line:
                    errors.append(f"ATTRIBUTE ERROR: {line.strip()}")
                elif 'clean_tts' in line.lower():
                    print(f"🔍 CLEAN_TTS LOG: {line.strip()}")
                
                if "Application startup complete" in line:
                    server_ready = True
                    
            if process.poll() is not None:
                break
    
    log_thread = threading.Thread(target=capture_logs, daemon=True)
    log_thread.start()
    
    # Aguardar servidor
    print("⏳ Aguardando servidor inicializar...")
    timeout = 60
    start_time = time.time()
    
    while not server_ready and (time.time() - start_time) < timeout:
        time.sleep(1)
    
    if not server_ready:
        print("❌ Servidor não inicializou em 60 segundos")
        process.terminate()
        return logs, errors
    
    print("✅ Servidor inicializado!")
    time.sleep(3)
    
    # Testar endpoint
    print("\n🧪 Testando endpoint de clonagem...")
    
    test_data = {
        "text": "Teste de integração do sistema limpo",
        "voice_name": "Julia",
        "language": "pt"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/tts/test-clone",
            json=test_data,
            timeout=60
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📊 Resultado: {result}")
        else:
            print(f"❌ Erro: {response.text}")
            errors.append(f"API ERROR: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        errors.append(f"REQUEST ERROR: {e}")
    
    # Aguardar mais logs
    print("\n⏳ Aguardando logs finais...")
    time.sleep(10)
    
    # Parar servidor
    print("\n🛑 Parando servidor...")
    process.terminate()
    time.sleep(2)
    if process.poll() is None:
        process.kill()
    
    return logs, errors

def analyze_coquitts_basic_vs_current():
    """Compara a implementação do coquittsbasic com a atual"""
    
    print("\n🔍 COMPARANDO COQUITTS BASIC VS IMPLEMENTAÇÃO ATUAL")
    print("=" * 60)
    
    # Verificar estrutura do coquittsbasic
    coqui_app_path = "coquittsbasic/app_basic.py"
    if os.path.exists(coqui_app_path):
        with open(coqui_app_path, 'r', encoding='utf-8') as f:
            coqui_content = f.read()
        
        print("📋 CARACTERÍSTICAS DO COQUITTS BASIC:")
        
        # Verificar características principais
        if 'TTS.api import TTS' in coqui_content:
            print("✅ Usa TTS.api diretamente")
        
        if 'tts_models/multilingual/multi-dataset/xtts_v2' in coqui_content:
            print("✅ Usa XTTS v2 como modelo principal")
        
        if 'speaker_wav=[referencia_path]' in coqui_content:
            print("✅ Usa speaker_wav como lista (método correto)")
        
        if 'COQUI_TOS_AGREED' in coqui_content:
            print("✅ Configura COQUI_TOS_AGREED=1")
        
        # Verificar método de clonagem
        if 'tts.tts_to_file(' in coqui_content:
            print("✅ Usa tts.tts_to_file() para clonagem")
            
            # Extrair exemplo de uso
            lines = coqui_content.split('\n')
            for i, line in enumerate(lines):
                if 'tts.tts_to_file(' in line:
                    print(f"\n🔍 MÉTODO DE CLONAGEM NO COQUITTS BASIC:")
                    for j in range(max(0, i-2), min(len(lines), i+8)):
                        print(f"   {lines[j]}")
                    break
    else:
        print("❌ coquittsbasic/app_basic.py não encontrado")
    
    # Verificar implementação atual
    clean_tts_path = "backend/clean_tts_service.py"
    if os.path.exists(clean_tts_path):
        with open(clean_tts_path, 'r', encoding='utf-8') as f:
            clean_content = f.read()
        
        print(f"\n📋 CARACTERÍSTICAS DA IMPLEMENTAÇÃO ATUAL:")
        
        if 'TTS.api import TTS' in clean_content:
            print("✅ Usa TTS.api")
        else:
            print("❌ Não usa TTS.api")
        
        if 'speaker_wav=[reference_path]' in clean_content:
            print("✅ Usa speaker_wav como lista")
        else:
            print("❌ Não usa speaker_wav como lista")
        
        if 'COQUI_TOS_AGREED' in clean_content:
            print("✅ Configura COQUI_TOS_AGREED")
        else:
            print("❌ Não configura COQUI_TOS_AGREED")

def main():
    print("🔧 DIAGNÓSTICO DE PROBLEMAS DE INTEGRAÇÃO")
    print("=" * 70)
    
    # 1. Verificar integração
    integration_ok = check_clean_tts_integration()
    
    # 2. Comparar implementações
    analyze_coquitts_basic_vs_current()
    
    # 3. Testar servidor
    logs, errors = test_server_with_logs()
    
    # 4. Análise final
    print("\n" + "=" * 70)
    print("📋 DIAGNÓSTICO FINAL:")
    print("=" * 70)
    
    if not integration_ok:
        print("❌ PROBLEMA: Integração do CleanTTSService falhou")
        print("💡 SOLUÇÃO: Re-executar python integrate_coquitts_basic.py")
    
    if errors:
        print(f"\n❌ ERROS ENCONTRADOS ({len(errors)}):")
        for error in errors[:5]:  # Mostrar apenas os primeiros 5
            print(f"   • {error}")
    
    # Verificar se o problema é de integração
    clean_tts_logs = [log for log in logs if 'clean_tts' in log.lower()]
    if not clean_tts_logs:
        print("\n❌ PROBLEMA IDENTIFICADO: CleanTTSService não está sendo usado!")
        print("💡 O sistema ainda está usando a implementação antiga")
        print("💡 SOLUÇÃO: Aplicar correções completas no main_enhanced.py")
    
    print("\n" + "=" * 70)
    print("🎯 PRÓXIMOS PASSOS:")
    print("=" * 70)
    print("1. Verificar se clean_tts_service.py existe e está correto")
    print("2. Verificar se main_enhanced.py importa e usa CleanTTSService")
    print("3. Re-aplicar integração se necessário")
    print("4. Testar novamente")
    print("=" * 70)

if __name__ == "__main__":
    main()