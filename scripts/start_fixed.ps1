# PowerShell script pentru Windows
Write-Host "🚀 Starting Discord Bot in Docker..." -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found! Please create it from .env.example" -ForegroundColor Red
    exit 1
}

# Check if n8n network exists
$networkExists = docker network ls | Select-String "n8n_n8n-network"
if (-not $networkExists) {
    Write-Host "⚠️ n8n network not found. Creating a default network..." -ForegroundColor Yellow
    docker network create n8n_n8n-network 2>$null
}

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down --remove-orphans 2>$null

# Start production environment
Write-Host "🚀 Starting production environment..." -ForegroundColor Green
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    # Wait for containers to be ready
    Write-Host "⏳ Waiting for containers to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Check container status
    Write-Host "📊 Container status:" -ForegroundColor Cyan
    docker-compose ps
    
    # Check logs
    Write-Host "📋 Recent logs:" -ForegroundColor Cyan
    docker-compose logs --tail=20 discord-bot
    
    Write-Host ""
    Write-Host "✅ Discord Bot started successfully!" -ForegroundColor Green
    Write-Host "📊 Check status: docker-compose ps" -ForegroundColor Yellow
    Write-Host "📋 View logs: docker-compose logs -f discord-bot" -ForegroundColor Yellow
    Write-Host "🔍 Health check: http://localhost:8002/health" -ForegroundColor Yellow
} else {
    Write-Host "❌ Failed to start Discord Bot" -ForegroundColor Red
}
