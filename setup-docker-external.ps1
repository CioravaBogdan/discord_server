# Docker Setup Script pentru Discord Bot
# Builds și pornește containerul cu webhook extern

Write-Host "=== Docker Discord Bot Setup ===" -ForegroundColor Green

# Verifică dacă Docker este instalat
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker nu este instalat sau nu este în PATH" -ForegroundColor Red
    Write-Host "Te rog instalează Docker Desktop și încearcă din nou" -ForegroundColor Yellow
    Read-Host "Apasă Enter pentru a ieși..."
    exit 1
}

# Verifică dacă Docker rulează
try {
    docker version | Out-Null
} catch {
    Write-Host "❌ Docker nu rulează. Te rog pornește Docker Desktop" -ForegroundColor Red
    Read-Host "Apasă Enter pentru a ieși..."
    exit 1
}

Write-Host "✅ Docker este disponibil" -ForegroundColor Green

# Setează locația proiectului
Set-Location "E:\Projects\BOT DISCORD"

# Verifică dacă .env există
if (!(Test-Path ".env")) {
    Write-Host "❌ Fișierul .env nu există!" -ForegroundColor Red
    Write-Host "Te rog configurează .env cu BOT_TOKEN și CHANNEL_ID" -ForegroundColor Yellow
    Read-Host "Apasă Enter pentru a ieși..."
    exit 1
}

Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker build -t infant-discord-bot .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to build Docker image" -ForegroundColor Red
    Read-Host "Apasă Enter pentru a ieși..."
    exit 1
}

Write-Host "🚀 Starting containers..." -ForegroundColor Yellow
docker-compose -f docker-compose-external.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Containers started successfully" -ForegroundColor Green
    Write-Host "📡 Webhook configurat pentru: https://n8n.byinfant.com/webhook/infant-discord-webhook" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Comenzi utile:" -ForegroundColor Yellow
    Write-Host "  - Vezi logs: docker-compose -f docker-compose-external.yml logs -f discord-bot" -ForegroundColor White
    Write-Host "  - Oprește: docker-compose -f docker-compose-external.yml down" -ForegroundColor White
    Write-Host "  - Restart: docker-compose -f docker-compose-external.yml restart discord-bot" -ForegroundColor White
} else {
    Write-Host "❌ Failed to start containers" -ForegroundColor Red
}

Read-Host "Apasă Enter pentru a continua..."
