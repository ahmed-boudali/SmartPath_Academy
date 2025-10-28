# SmartPath Academy - Quick Start Script (Windows)

Write-Host "🚀 Starting SmartPath Academy..." -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please update .env with your configuration!" -ForegroundColor Yellow
}

# Build and start services
Write-Host "🐳 Building Docker containers..." -ForegroundColor Cyan
docker-compose up --build -d

# Wait for database to be ready
Write-Host "⏳ Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run migrations
Write-Host "📊 Running database migrations..." -ForegroundColor Cyan
docker-compose exec web python manage.py migrate

# Collect static files
Write-Host "📦 Collecting static files..." -ForegroundColor Cyan
docker-compose exec web python manage.py collectstatic --noinput

Write-Host ""
Write-Host "✅ SmartPath Academy is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access points:" -ForegroundColor Cyan
Write-Host "   - API: http://localhost:8000"
Write-Host "   - Admin: http://localhost:8000/admin"
Write-Host "   - Swagger: http://localhost:8000/swagger"
Write-Host "   - ReDoc: http://localhost:8000/redoc"
Write-Host ""
Write-Host "👤 Create superuser with:" -ForegroundColor Yellow
Write-Host "   docker-compose exec web python manage.py createsuperuser"
