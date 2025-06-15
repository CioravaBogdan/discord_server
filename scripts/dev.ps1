# PowerShell script pentru development
Write-Host "🛠️ Starting Discord Bot in development mode..." -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found! Please create it from .env.example" -ForegroundColor Red
    exit 1
}

# Start development environment
Write-Host "🔧 Starting development environment..." -ForegroundColor Green
docker-compose -f docker-compose.dev.yml up --build

Write-Host "🔧 Development environment ready!" -ForegroundColor Green
