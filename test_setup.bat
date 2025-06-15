@echo off
echo.
echo =================================================
echo    Discord Bot cu n8n - Test de Conectivitate
echo =================================================
echo.

echo 1. Verificare n8n Docker...
curl -X GET "http://localhost:5678" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ n8n este accesibil pe portul 5678
) else (
    echo ❌ n8n nu este accesibil. Verifică că Docker rulează cu n8n
)

echo.
echo 2. Test webhook n8n...
curl -X POST "http://localhost:5678/webhook/discord-bot" ^
     -H "Content-Type: application/json" ^
     -d "{\"test\": \"connection from Discord bot\"}" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Webhook n8n răspunde
) else (
    echo ❌ Webhook-ul n8n nu răspunde. Creează workflow în n8n cu webhook
)

echo.
echo 3. Verificare configurație...
if exist .env (
    echo ✅ Fișierul .env există
    echo.
    echo Configurația curentă:
    type .env
) else (
    echo ❌ Fișierul .env nu există
)

echo.
echo =================================================
echo            Pași pentru configurare:
echo =================================================
echo 1. Asigură-te că n8n rulează în Docker pe portul 5678
echo 2. Creează un workflow în n8n cu webhook pe /discord-bot
echo 3. Actualizează CHANNEL_ID în .env cu ID-ul real
echo 4. Rulează: python main.py
echo =================================================
pause
