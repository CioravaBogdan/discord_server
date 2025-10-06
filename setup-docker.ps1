# Discord Bot + n8n Docker Setup pentru Windows 10
# Acest script configurează și pornește întreaga aplicație în Docker

Write-Host "🚀 Discord Bot + n8n Docker Setup pentru Windows 10" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan

# Verifică dacă Docker este instalat și rulează
Write-Host "`n📋 Verificare prerequisite..." -ForegroundColor Yellow

try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker instalat: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker nu este instalat sau nu rulează!" -ForegroundColor Red
    Write-Host "Te rog instalează Docker Desktop pentru Windows." -ForegroundColor Red
    exit 1
}

# Verifică dacă Docker Compose este disponibil
try {
    $dockerComposeVersion = docker compose version
    Write-Host "✅ Docker Compose disponibil: $dockerComposeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose nu este disponibil!" -ForegroundColor Red
    exit 1
}

# Verifică fișierul .env
if (Test-Path ".env") {
    Write-Host "✅ Fișier .env găsit" -ForegroundColor Green
} else {
    Write-Host "❌ Fișierul .env nu există!" -ForegroundColor Red
    Write-Host "Te rog copiază .env.example ca .env și completează-l." -ForegroundColor Red
    exit 1
}

# Creează directoarele necesare
Write-Host "`n📁 Creez directoarele necesare..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
New-Item -ItemType Directory -Force -Path "data" | Out-Null
Write-Host "✅ Directoare create: logs/, data/" -ForegroundColor Green

# Oprește containerele existente dacă rulează
Write-Host "`n🛑 Opresc containerele existente..." -ForegroundColor Yellow
docker compose down 2>$null
Write-Host "✅ Containerele existente au fost oprite" -ForegroundColor Green

# Construiește imaginile
Write-Host "`n🔨 Construiesc imaginile Docker..." -ForegroundColor Yellow
$buildResult = docker compose build --no-cache
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Imaginile au fost construite cu succes" -ForegroundColor Green
} else {
    Write-Host "❌ Eroare la construirea imaginilor!" -ForegroundColor Red
    exit 1
}

# Pornește serviciile
Write-Host "`n🚀 Pornesc serviciile..." -ForegroundColor Yellow
$startResult = docker compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Serviciile au fost pornite cu succes" -ForegroundColor Green
} else {
    Write-Host "❌ Eroare la pornirea serviciilor!" -ForegroundColor Red
    exit 1
}

# Așteaptă ca serviciile să pornească
Write-Host "`n⏳ Aștept ca serviciile să pornească (30 secunde)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verifică statusul serviciilor
Write-Host "`n📊 Status servicii:" -ForegroundColor Cyan
docker compose ps

# Testează conectivitatea
Write-Host "`n🧪 Testez conectivitatea..." -ForegroundColor Yellow

# Test n8n
try {
    $n8nResponse = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 10 -UseBasicParsing
    Write-Host "✅ n8n răspunde pe http://localhost:5678" -ForegroundColor Green
} catch {
    Write-Host "⚠️  n8n nu răspunde încă (normal în primul setup)" -ForegroundColor Yellow
}

# Test Discord bot webhook
try {
    $botResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10 -UseBasicParsing
    Write-Host "✅ Discord bot webhook răspunde pe http://localhost:8000" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Discord bot webhook nu răspunde încă" -ForegroundColor Yellow
}

Write-Host "`n🎉 Setup complet!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "📌 Servicii disponibile:" -ForegroundColor White
Write-Host "   • n8n Web Interface: http://localhost:5678" -ForegroundColor Cyan
Write-Host "   • Discord Bot Webhook: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   • Redis: localhost:6379" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 Comenzi utile:" -ForegroundColor White
Write-Host "   • Vezi logs: docker compose logs -f" -ForegroundColor Gray
Write-Host "   • Vezi status: docker compose ps" -ForegroundColor Gray
Write-Host "   • Oprește: docker compose down" -ForegroundColor Gray
Write-Host "   • Restart: docker compose restart" -ForegroundColor Gray
Write-Host ""
Write-Host "📌 Următorii pași:" -ForegroundColor White
Write-Host "   1. Deschide n8n la http://localhost:5678" -ForegroundColor Yellow
Write-Host "   2. Creează un workflow cu webhook 'infant-discord-webhook'" -ForegroundColor Yellow
Write-Host "   3. Testează bot-ul în Discord" -ForegroundColor Yellow

Write-Host "`nApasă orice tastă pentru a vedea logs-urile live..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Afișează logs live
Write-Host "`n📄 Logs live (Ctrl+C pentru a ieși):" -ForegroundColor Cyan
docker compose logs -f
