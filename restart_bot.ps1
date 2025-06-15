# Script pentru restart rapid al bot-ului Discord
Write-Host "🔄 Restart Discord Bot..." -ForegroundColor Cyan

# Oprește toate procesele Python care rulează bot-ul
Write-Host "🛑 Opresc bot-ul curent..." -ForegroundColor Yellow
Get-Process -Name "python*" -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match "python" -and $_.CommandLine -match "main.py|bot.py"
} | Stop-Process -Force -ErrorAction SilentlyContinue

# Așteaptă puțin pentru cleanup
Start-Sleep -Seconds 2

# Testează filtrarea
Write-Host "🧪 Testez filtrarea mesajelor..." -ForegroundColor Green
python test_filters.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Testele de filtrare au eșuat!" -ForegroundColor Red
    exit 1
}

# Pornește bot-ul
Write-Host "🚀 Pornesc bot-ul cu filtrare îmbunătățită..." -ForegroundColor Green
python main.py
