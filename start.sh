#!/bin/bash

# SmartPath Academy - Quick Start Script

echo "🚀 Starting SmartPath Academy..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration!"
fi

# Build and start services
echo "🐳 Building Docker containers..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "📊 Running database migrations..."
docker-compose exec web python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "✅ SmartPath Academy is ready!"
echo ""
echo "🌐 Access points:"
echo "   - API: http://localhost:8000"
echo "   - Admin: http://localhost:8000/admin"
echo "   - Swagger: http://localhost:8000/swagger"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "👤 Create superuser with:"
echo "   docker-compose exec web python manage.py createsuperuser"
