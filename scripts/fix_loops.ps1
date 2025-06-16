# PowerShell script pentru restart rapid cu testare
Write-Host "🔧 Fixing Discord bot message loops..." -ForegroundColor Cyan

# Test filtering first
Write-Host "Testing enhanced filtering..." -ForegroundColor Yellow
python test_enhanced_filtering.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Filtering tests passed, restarting bot..." -ForegroundColor Green
    docker-compose down
    docker-compose build --no-cache discord-bot
    docker-compose up -d
    
    # Wait for startup
    Start-Sleep -Seconds 10
    
    # Show status
    Write-Host "📊 Container status:" -ForegroundColor Cyan
    docker-compose ps
    
    # Show recent logs
    Write-Host "📋 Recent logs:" -ForegroundColor Cyan
    docker-compose logs --tail=15 discord-bot
    
    Write-Host "✅ Bot restarted with enhanced filtering!" -ForegroundColor Green
} else {
    Write-Host "❌ Filtering tests failed, please check configuration" -ForegroundColor Red
    exit 1
}
