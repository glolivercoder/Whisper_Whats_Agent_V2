@echo off
title Port Cleanup Utility - WhatsApp Voice Agent V2
color 0C

echo ========================================
echo  🧹 Port Cleanup Utility
echo  🎯 Targeting Ports 8001 and 8002
echo ========================================
echo.

echo 🔍 Checking active connections on ports 8001 and 8002...
echo.

:: Show current port usage
echo 📊 Current port usage:
netstat -ano | findstr ":800" | findstr "LISTENING"
echo.

:: Force kill processes on port 8001
echo 🛑 Terminating processes on port 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001" 2^>nul') do (
    echo   Killing PID: %%a
    taskkill /f /pid %%a >nul 2>&1
)

:: Force kill processes on port 8002
echo 🛑 Terminating processes on port 8002...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8002" 2^>nul') do (
    echo   Killing PID: %%a
    taskkill /f /pid %%a >nul 2>&1
)

:: Additional Python server cleanup
echo 🐍 Cleaning up Python server processes...
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" /fo csv 2^>nul ^| find "python.exe"') do (
    for /f "tokens=1" %%b in ('netstat -ano ^| findstr ":800" ^| findstr %%a 2^>nul') do (
        echo   Terminating Python PID: %%a
        taskkill /f /pid %%a >nul 2>&1
    )
)

echo.
echo ⏳ Waiting for cleanup to complete...
timeout /t 3 /nobreak >nul

echo.
echo 🔍 Verifying cleanup...
netstat -ano | findstr ":800" | findstr "LISTENING" >nul 2>&1
if errorlevel 1 (
    echo ✅ All ports cleaned successfully!
) else (
    echo ⚠️  Some processes may still be running:
    netstat -ano | findstr ":800" | findstr "LISTENING"
)

echo.
echo 🎯 Cleanup completed. You can now start the server.
echo.
pause