# Test script pentru Docker setup
Write-Host "🧪 Test Discord Bot + n8n Docker Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

$testsPassed = 0
$totalTests = 6

# Test 1: Docker status
Write-Host "`n1. Test Docker status..." -ForegroundColor Yellow
try {
    $containers = docker compose ps --format json | ConvertFrom-Json
    $runningContainers = $containers | Where-Object { $_.State -eq "running" }
    
    if ($runningContainers.Count -ge 3) {
        Write-Host "✅ Toate containerele rulează ($($runningContainers.Count)/3)" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Nu toate containerele rulează ($($runningContainers.Count)/3)" -ForegroundColor Red
        Write-Host "Containere care rulează:" -ForegroundColor Gray
        $runningContainers | ForEach-Object { Write-Host "  - $($_.Name): $($_.State)" -ForegroundColor Gray }
    }
} catch {
    Write-Host "❌ Eroare la verificarea containerelor: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: n8n web interface
Write-Host "`n2. Test n8n web interface..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ n8n web interface funcționează (http://localhost:5678)" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ n8n nu răspunde corect (Status: $($response.StatusCode))" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ n8n nu este accesibil: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Discord bot health check
Write-Host "`n3. Test Discord bot health check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Discord bot health check OK (http://localhost:8000/health)" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Discord bot health check failed (Status: $($response.StatusCode))" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Discord bot nu răspunde: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Redis connectivity
Write-Host "`n4. Test Redis connectivity..." -ForegroundColor Yellow
try {
    $redisTest = docker compose exec -T redis redis-cli ping
    if ($redisTest.Trim() -eq "PONG") {
        Write-Host "✅ Redis funcționează" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Redis nu răspunde la ping" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Eroare la testarea Redis: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Discord bot API endpoint
Write-Host "`n5. Test Discord bot API endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Discord bot API endpoint funcționează" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Discord bot API nu răspunde corect" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Discord bot API nu este accesibil: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Environment configuration
Write-Host "`n6. Test environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    $requiredVars = @("BOT_TOKEN", "CHANNEL_ID", "N8N_WEBHOOK")
    $missingVars = @()
    
    foreach ($var in $requiredVars) {
        if ($envContent -notmatch "$var=.+") {
            $missingVars += $var
        }
    }
    
    if ($missingVars.Count -eq 0) {
        Write-Host "✅ Toate variabilele de environment sunt configurate" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Variabile lipsă în .env: $($missingVars -join ', ')" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Fișierul .env nu există" -ForegroundColor Red
}

# Rezultate finale
Write-Host "`n📊 Rezultate finale:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host "Teste trecute: $testsPassed/$totalTests" -ForegroundColor $(if ($testsPassed -eq $totalTests) { "Green" } else { "Yellow" })

if ($testsPassed -eq $totalTests) {
    Write-Host "`n🎉 TOATE TESTELE AU TRECUT! Aplicația este gata de utilizare." -ForegroundColor Green
    Write-Host "`n📌 Următorii pași:" -ForegroundColor White
    Write-Host "1. Deschide n8n: http://localhost:5678" -ForegroundColor Cyan
    Write-Host "2. Creează un workflow cu webhook 'infant-discord-webhook'" -ForegroundColor Cyan
    Write-Host "3. Testează bot-ul în Discord" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️  UNELE TESTE AU EȘUAT. Verifică erorile de mai sus." -ForegroundColor Yellow
    Write-Host "`n📌 Acțiuni recomandate:" -ForegroundColor White
    Write-Host "1. Verifică logs-urile: docker compose logs -f" -ForegroundColor Gray
    Write-Host "2. Restart serviciile: docker compose restart" -ForegroundColor Gray
    Write-Host "3. Verifică configurația .env" -ForegroundColor Gray
}

Write-Host "`n📄 Pentru logs detaliate rulează: docker compose logs -f" -ForegroundColor Gray
