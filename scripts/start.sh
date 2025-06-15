#!/bin/bash
set -e

echo "🚀 Starting Discord Bot in Docker..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found! Please create it from .env.example"
    exit 1
fi

# Check if n8n network exists
if ! docker network ls | grep -q "n8n_n8n-network"; then
    echo "⚠️ n8n network not found. Creating a default network..."
    docker network create n8n_n8n-network || true
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans || true

# Start production environment
echo "🚀 Starting production environment..."
docker-compose up -d

# Wait for containers to be ready
echo "⏳ Waiting for containers to be ready..."
sleep 10

# Check container status
echo "📊 Container status:"
docker-compose ps

# Check logs
echo "📋 Recent logs:"
docker-compose logs --tail=20 discord-bot

echo ""
echo "✅ Discord Bot started successfully!"
echo "📊 Check status: docker-compose ps"
echo "📋 View logs: docker-compose logs -f discord-bot"
echo "🔍 Health check: curl http://localhost:8002/health"
