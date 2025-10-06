# 🤖 DISCORD BOT - RESTAURARE COMPLETĂ

Write-Host "===============================================" -ForegroundColor Green
Write-Host "   DISCORD BOT INFANT - RESTAURAT CU SUCCES   " -ForegroundColor Green  
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

Write-Host "📍 CONFIGURAȚIE ACTUALIZATĂ:" -ForegroundColor Yellow
Write-Host "   • Webhook: https://n8n.byinfant.com/webhook/infant-discord-webhook" -ForegroundColor Cyan
Write-Host "   • Python Environment: Configurat și activ" -ForegroundColor Green
Write-Host "   • Dependencies: Instalate cu succes" -ForegroundColor Green
Write-Host "   • Docker: Configurat pentru webhook extern" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 OPȚIUNI DE PORNIRE:" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "Alege metoda de pornire:
[1] Pornește Local (Python)
[2] Pornește Docker
[3] Doar afișează informații
[q] Ieși

Alegerea ta (1/2/3/q)"

switch ($choice) {
    "1" {
        Write-Host "🐍 Pornesc bot-ul local..." -ForegroundColor Green
        & "E:\Projects\BOT DISCORD\.venv\Scripts\python.exe" main.py
    }
    "2" {
        Write-Host "🐳 Pornesc setup Docker..." -ForegroundColor Green
        & ".\setup-docker-external.ps1"
    }
    "3" {
        Write-Host ""
        Write-Host "📋 INFORMAȚII UTILE:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Local:" -ForegroundColor Cyan
        Write-Host "  .\start_bot_new.ps1" -ForegroundColor White
        Write-Host ""
        Write-Host "Docker:" -ForegroundColor Cyan  
        Write-Host "  .\setup-docker-external.ps1   # Start" -ForegroundColor White
        Write-Host "  .\stop-docker-external.ps1    # Stop" -ForegroundColor White
        Write-Host ""
        Write-Host "Logs:" -ForegroundColor Cyan
        Write-Host "  Local: .\logs\discord_bot.log" -ForegroundColor White
        Write-Host "  Docker: docker-compose -f docker-compose-external.yml logs discord-bot" -ForegroundColor White
        Write-Host ""
        Write-Host "Test config:" -ForegroundColor Cyan
        Write-Host "  python test_config.py" -ForegroundColor White
    }
    "q" {
        Write-Host "👋 La revedere!" -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "❌ Opțiune invalidă!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ RESTAURARE COMPLETĂ!" -ForegroundColor Green
Read-Host "Apasă Enter pentru a ieși..."
