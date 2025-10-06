# Script pentru oprirea Discord Bot + n8n Docker

Write-Host "🛑 Opresc Discord Bot + n8n..." -ForegroundColor Yellow

# Oprește și șterge containerele
docker compose down

# Opțional: șterge și volumele (dacă vrei să ștergi toate datele)
$deleteVolumes = Read-Host "Vrei să ștergi și datele salvate? (y/N)"
if ($deleteVolumes -eq "y" -or $deleteVolumes -eq "Y") {
    Write-Host "🗑️  Șterg volumele..." -ForegroundColor Red
    docker compose down -v
    docker volume prune -f
    Write-Host "✅ Volumele au fost șterse" -ForegroundColor Green
}

# Verifică dacă mai sunt containere care rulează
$runningContainers = docker ps --filter "name=infant-" --format "table {{.Names}}\t{{.Status}}"
if ($runningContainers) {
    Write-Host "⚠️  Containere care încă rulează:" -ForegroundColor Yellow
    Write-Host $runningContainers
} else {
    Write-Host "✅ Toate containerele au fost oprite" -ForegroundColor Green
}

Write-Host "`nPentru a porni din nou: .\setup-docker.ps1" -ForegroundColor Cyan
