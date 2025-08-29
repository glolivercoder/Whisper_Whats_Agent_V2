@echo off
echo ========================================
echo  REINICIANDO SERVIDOR COM CORREÇÕES TTS
echo ========================================
echo.

echo 🔄 Parando processos existentes na porta 8001...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8001" ^| find "LISTENING"') do (
    echo   🛑 Matando processo %%a
    taskkill /f /pid %%a >nul 2>&1
)

echo.
echo ⏳ Aguardando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo 🚀 Iniciando servidor com correções aplicadas...
echo 💡 Pressione Ctrl+C para parar o servidor
echo.

python backend/main_enhanced.py

echo.
echo 🏁 Servidor parado.
pause