@echo off
title Discord Bot + n8n - Status Check
color 0A

echo.
echo ================================
echo   DISCORD BOT + n8n STATUS
echo ================================
echo.

echo 1. Verificare n8n Docker...
curl -s http://localhost:5678 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ n8n rulează pe portul 5678
) else (
    echo ❌ n8n nu este accesibil - verifică Docker
    goto :end
)

echo.
echo 2. Verificare webhook n8n...
curl -s -X POST "http://localhost:5678/webhook/discord-bot" -H "Content-Type: application/json" -d "{\"test\":\"ok\"}" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Webhook n8n răspunde
) else (
    echo ❌ Webhook discord-bot nu există în n8n
    echo   Creează workflow cu webhook path: discord-bot
)

echo.
echo 3. Verificare configurație .env...
if exist .env (
    echo ✅ Fișier .env găsit
    echo.
    echo Configurația curentă:
    type .env
) else (
    echo ❌ Fișierul .env lipsește
)

echo.
echo 4. Verificare dependențe Python...
py -c "import discord, fastapi, requests; print('✅ Toate dependențele sunt instalate')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Dependențe lipsă - rulează: py -m pip install -r requirements.txt
)

echo.
echo ================================
echo        URMĂTORII PAȘI:
echo ================================
echo 1. Deschide n8n: http://localhost:5678
echo 2. Creează workflow cu webhook "discord-bot"
echo 3. Obține Channel ID din Discord
echo 4. Actualizează CHANNEL_ID în .env
echo 5. Rulează: start_bot.bat
echo ================================

:end
echo.
pause
