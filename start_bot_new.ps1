# Discord Bot Starter Script
# Activează environment-ul și pornește bot-ul

Write-Host "=== Discord Bot Starter ===" -ForegroundColor Green
Write-Host "Activez Python environment..." -ForegroundColor Yellow

# Setează locația corectă
Set-Location "E:\Projects\BOT DISCORD"

# Activează virtual environment
& "E:\Projects\BOT DISCORD\.venv\Scripts\Activate.ps1"

Write-Host "Environment activat. Pornesc bot-ul..." -ForegroundColor Yellow
Write-Host "Webhook configurat pentru: https://n8n.byinfant.com/webhook/infant-discord-webhook" -ForegroundColor Cyan

# Pornește bot-ul
& "E:\Projects\BOT DISCORD\.venv\Scripts\python.exe" main.py

Write-Host "Bot-ul s-a oprit." -ForegroundColor Red
Read-Host "Apasă Enter pentru a închide..."
