# Script pentru oprirea containerelor Docker

Write-Host "=== Oprire Discord Bot Docker ===" -ForegroundColor Yellow

Set-Location "E:\Projects\BOT DISCORD"

Write-Host "🛑 Opresc containerele..." -ForegroundColor Yellow
docker-compose -f docker-compose-external.yml down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Containerele au fost oprite" -ForegroundColor Green
} else {
    Write-Host "❌ Eroare la oprirea containerelor" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Comenzi suplimentare:" -ForegroundColor Yellow
Write-Host "  - Șterge volumes: docker-compose -f docker-compose-external.yml down -v" -ForegroundColor White
Write-Host "  - Șterge images: docker rmi infant-discord-bot" -ForegroundColor White

Read-Host "Apasă Enter pentru a ieși..."
