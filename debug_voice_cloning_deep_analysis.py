#!/usr/bin/env python3
"""
Análise profunda dos problemas na clonagem de voz
"""

import os
import sys
import requests
import json
import subprocess
import time
import threading
from datetime import datetime

def check_reference_audio_files():
    """Verifica se existem arquivos de referência para clonagem"""
    print("🔍 Verificando arquivos de referência de áudio...")
    
    reference_dirs = [
        "reference_audio",
        "backend/reference_audio",
        "cloned_voices", 
        "backend/cloned_voices"
    ]
    
    found_files = []
    
    for directory in reference_dirs:
        if os.path.exists(directory):
            print(f"   📁 Diretório encontrado: {directory}")
            files = [f for f in os.listdir(directory) if f.endswith(('.wav', '.mp3', '.flac'))]
            if files:
                print(f"      Arquivos de áudio: {len(files)}")
                for file in files:
                    file_path = os.path.join(directory, file)
                    file_size = os.path.getsize(file_path)
                    print(f"      • {file} ({file_size} bytes)")
                    found_files.append(file_path)
            else:
                print(f"      ❌ Nenhum arquivo de áudio encontrado")
        else:
            print(f"   ❌ Diretório não existe: {directory}")
    
    if not found_files:
        print("\n❌ PROBLEMA CRÍTICO: Nenhum arquivo de referência encontrado!")
        print("💡 A clonagem de voz precisa de arquivos de referência (.wav, .mp3)")
        return False
    
    print(f"\n✅ Total de arquivos de referência: {len(found_files)}")
    return True

def check_xtts_v2_installation():
    """Verifica se o XTTS v2 está instalado corretamente"""
    print("\n🔍 Verificando instalação do XTTS v2...")
    
    try:
        sys.path.append('backend')
        from TTS.api import TTS
        
        print("✅ TTS importado com sucesso")
        
        # Tentar carregar XTTS v2
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        print(f"   Testando modelo: {model_name}")
        
        tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
        print("✅ XTTS v2 carregado com sucesso")
        
        # Verificar idiomas suportados
        if hasattr(tts, 'languages'):
            languages = tts.languages
            print(f"   Idiomas suportados: {languages}")
            if 'pt' in languages:
                print("✅ Português (pt) suportado")
            else:
                print("❌ Português (pt) não encontrado nos idiomas suportados")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação TTS: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro ao carregar XTTS v2: {e}")
        return False

def analyze_server_logs_detailed():
    """Analisa os logs do servidor em detalhes"""
    print("\n🔍 Iniciando análise detalhada dos logs do servidor...")
    
    # Iniciar servidor e capturar todos os logs
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
    
    def capture_logs():
        nonlocal server_ready, logs
        while True:
            line = process.stdout.readline()
            if line:
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                log_entry = f"[{timestamp}] {line.strip()}"
                logs.append(log_entry)
                print(log_entry)
                
                if "Application startup complete" in line:
                    server_ready = True
                    
            if process.poll() is not None:
                break
    
    log_thread = threading.Thread(target=capture_logs, daemon=True)
    log_thread.start()
    
    # Aguardar servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    timeout = 60
    start_time = time.time()
    
    while not server_ready and (time.time() - start_time) < timeout:
        time.sleep(1)
    
    if not server_ready:
        print("❌ Servidor não inicializou em 60 segundos")
        process.terminate()
        return None, logs
    
    print("✅ Servidor inicializado, aguardando mais 3 segundos...")
    time.sleep(3)
    
    # Fazer requisição de teste
    print("\n🧪 Fazendo requisição de teste para clonagem...")
    
    test_data = {
        "text": "Teste de clonagem de voz em português.",
        "voice_name": "crianca",
        "language": "pt"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/tts/test-clone",
            json=test_data,
            timeout=60
        )
        
        print(f"📥 Resposta da requisição:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Resposta JSON: {json.dumps(result, indent=2)}")
        else:
            print(f"   Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Aguardar mais logs
    print("\n⏳ Aguardando logs adicionais por 10 segundos...")
    time.sleep(10)
    
    # Parar servidor
    print("\n🛑 Parando servidor...")
    process.terminate()
    time.sleep(2)
    if process.poll() is None:
        process.kill()
    
    return response if 'response' in locals() else None, logs

def analyze_logs_for_errors(logs):
    """Analisa os logs em busca de erros específicos"""
    print("\n🔍 Analisando logs em busca de erros...")
    
    error_patterns = {
        "Language not supported": r"Language .* is not supported",
        "File not found": r"FileNotFoundError|No such file",
        "Permission denied": r"PermissionError|Permission denied",
        "CUDA/GPU error": r"CUDA|GPU|torch",
        "Import error": r"ImportError|ModuleNotFoundError",
        "Audio processing": r"audio|wav|mp3",
        "XTTS error": r"XTTS|xtts",
        "Cloning error": r"clone|cloning",
        "Memory error": r"MemoryError|OutOfMemoryError",
        "Timeout": r"timeout|Timeout"
    }
    
    found_errors = {}
    
    for log in logs:
        for error_type, pattern in error_patterns.items():
            import re
            if re.search(pattern, log, re.IGNORECASE):
                if error_type not in found_errors:
                    found_errors[error_type] = []
                found_errors[error_type].append(log)
    
    if found_errors:
        print("❌ Erros encontrados nos logs:")
        for error_type, error_logs in found_errors.items():
            print(f"\n   🔴 {error_type}:")
            for error_log in error_logs[:3]:  # Mostrar apenas os primeiros 3
                print(f"      {error_log}")
    else:
        print("✅ Nenhum erro óbvio encontrado nos logs")
    
    return found_errors

def diagnose_root_cause():
    """Diagnóstica a causa raiz do problema"""
    print("\n🎯 DIAGNÓSTICO DA CAUSA RAIZ")
    print("=" * 60)
    
    issues = []
    
    # 1. Verificar arquivos de referência
    if not check_reference_audio_files():
        issues.append({
            "type": "CRÍTICO",
            "problem": "Arquivos de referência ausentes",
            "solution": "Criar diretório reference_audio/ com arquivos .wav de exemplo"
        })
    
    # 2. Verificar XTTS v2
    if not check_xtts_v2_installation():
        issues.append({
            "type": "CRÍTICO", 
            "problem": "XTTS v2 não instalado ou com problemas",
            "solution": "Reinstalar TTS: pip install TTS"
        })
    
    # 3. Analisar logs do servidor
    response, logs = analyze_server_logs_detailed()
    
    # 4. Analisar erros nos logs
    log_errors = analyze_logs_for_errors(logs)
    
    for error_type, error_logs in log_errors.items():
        issues.append({
            "type": "ERRO",
            "problem": f"Erro nos logs: {error_type}",
            "solution": f"Verificar: {error_logs[0] if error_logs else 'N/A'}"
        })
    
    # 5. Verificar resposta da API
    if response:
        if response.status_code != 200:
            issues.append({
                "type": "API",
                "problem": f"API retornou status {response.status_code}",
                "solution": f"Verificar endpoint e dados: {response.text}"
            })
    
    return issues

def main():
    print("🔧 ANÁLISE PROFUNDA DOS PROBLEMAS DE CLONAGEM DE VOZ")
    print("=" * 70)
    
    issues = diagnose_root_cause()
    
    print("\n" + "=" * 70)
    print("📋 RESUMO DOS PROBLEMAS ENCONTRADOS:")
    print("=" * 70)
    
    if not issues:
        print("✅ Nenhum problema crítico identificado")
        print("💡 O sistema deveria estar funcionando")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. [{issue['type']}] {issue['problem']}")
            print(f"   💡 Solução: {issue['solution']}")
    
    print("\n" + "=" * 70)
    print("🎯 PRÓXIMOS PASSOS RECOMENDADOS:")
    print("=" * 70)
    
    if any(issue['type'] == 'CRÍTICO' for issue in issues):
        print("1. Resolver problemas CRÍTICOS primeiro")
        print("2. Criar arquivos de referência se necessário")
        print("3. Verificar instalação do TTS")
    else:
        print("1. Verificar logs detalhados acima")
        print("2. Testar com arquivo de referência específico")
        print("3. Verificar configurações de idioma")
    
    print("=" * 70)

if __name__ == "__main__":
    main()