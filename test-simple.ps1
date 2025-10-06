# Test script pentru Docker setup
Write-Host "Test Discord Bot + n8n Docker Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

$testsPassed = 0
$totalTests = 5

# Test 1: Docker container status
Write-Host "`n1. Test Docker container status..." -ForegroundColor Yellow
try {
    $result = docker ps --filter "name=infant-discord-bot" --format "{{.Status}}"
    if ($result -like "*Up*") {
        Write-Host "✅ Discord bot container is running" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Discord bot container is not running" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error checking container status: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: n8n web interface
Write-Host "`n2. Test n8n web interface..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ n8n web interface is working (http://localhost:5678)" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ n8n not responding correctly (Status: $($response.StatusCode))" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ n8n not accessible: $($_.Exception.Message)" -ForegroundColor Red
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
    Write-Host "❌ Discord bot not responding: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Discord bot API endpoint
Write-Host "`n4. Test Discord bot API endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Discord bot API endpoint is working" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Discord bot API not responding correctly" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Discord bot API not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Environment configuration
Write-Host "`n5. Test environment configuration..." -ForegroundColor Yellow
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
        Write-Host "✅ All environment variables are configured" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "❌ Missing variables in .env: $($missingVars -join ', ')" -ForegroundColor Red
    }
} else {
    Write-Host "❌ .env file does not exist" -ForegroundColor Red
}

# Final results
Write-Host "`nFinal Results:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host "Tests passed: $testsPassed/$totalTests" -ForegroundColor $(if ($testsPassed -eq $totalTests) { "Green" } else { "Yellow" })

if ($testsPassed -eq $totalTests) {
    Write-Host "`n🎉 ALL TESTS PASSED! Application is ready to use." -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor White
    Write-Host "1. Open n8n: http://localhost:5678" -ForegroundColor Cyan
    Write-Host "2. Create workflow with webhook 'infant-discord-webhook'" -ForegroundColor Cyan
    Write-Host "3. Test bot in Discord" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️  SOME TESTS FAILED. Check errors above." -ForegroundColor Yellow
    Write-Host "`nRecommended actions:" -ForegroundColor White
    Write-Host "1. Check logs: docker logs infant-discord-bot" -ForegroundColor Gray
    Write-Host "2. Restart services: docker compose -f docker-compose-simple.yml restart" -ForegroundColor Gray
    Write-Host "3. Check .env configuration" -ForegroundColor Gray
}

Write-Host "`nFor detailed logs run: docker logs infant-discord-bot" -ForegroundColor Gray
