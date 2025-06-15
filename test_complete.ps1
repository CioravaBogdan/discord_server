# Script PowerShell pentru testarea bot-ului Discord

Write-Host "🔧 Testare Bot Discord cu n8n" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Oprește procesele existente
Write-Host "`n1. Opresc procesele existente..." -ForegroundColor Yellow
Stop-Process -Name "py" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Pornește bot-ul
Write-Host "`n2. Pornesc bot-ul Discord..." -ForegroundColor Yellow
Start-Process py -ArgumentList "main.py" -NoNewWindow

# Așteaptă să pornească
Write-Host "   Aștept 5 secunde să pornească..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Testează conexiunea
Write-Host "`n3. Testez conexiunea..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ Bot status: $($health.bot_status)" -ForegroundColor Green
    Write-Host "✅ Webhook server: $($health.webhook_server)" -ForegroundColor Green
} catch {
    Write-Host "❌ Bot-ul nu răspunde!" -ForegroundColor Red
}

# Testează trimiterea unui mesaj
Write-Host "`n4. Testez trimiterea unui mesaj..." -ForegroundColor Yellow
$body = @{
    channel_id = 1383864616052068414
    content = "🎉 Bot Discord conectat! Integrare n8n funcțională!"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/send-message" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ Mesaj trimis cu succes!" -ForegroundColor Green
} catch {
    Write-Host "❌ Eroare la trimiterea mesajului: $_" -ForegroundColor Red
}

# Testează webhook-ul n8n
Write-Host "`n5. Testez webhook-ul n8n..." -ForegroundColor Yellow
$testData = @{
    content = "Test mesaj pentru n8n"
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ"
    message_id = "test_$(Get-Random)"
    channel = @{
        id = "1383864616052068414"
        name = "new-products"
    }
    author = @{
        id = "123456789"
        username = "test_bot"
        display_name = "Test Bot"
    }
    attachments = @()
} | ConvertTo-Json -Depth 3

try {
    $response = Invoke-RestMethod -Uri "https://n8n-api.logistics-lead.com/webhook-test/infant-discord-webhook" -Method Post -Body $testData -ContentType "application/json"
    Write-Host "✅ Webhook n8n a primit datele!" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "⚠️  Webhook-ul n8n nu este activ. Activează workflow-ul în n8n!" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Eroare webhook n8n: $_" -ForegroundColor Red
    }
}

Write-Host "`n✨ Test complet!" -ForegroundColor Cyan
Write-Host "Verifică canalul #new-products pe Discord pentru mesaj!" -ForegroundColor Cyan
