#!/bin/bash
set -e

echo "🛠️ Starting Discord Bot in development mode..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found! Please create it from .env.example"
    exit 1
fi

# Start development environment with hot reload
echo "🔧 Starting development environment..."
docker-compose -f docker-compose.dev.yml up --build

echo "🔧 Development environment started!"
echo "📊 Check status: docker-compose -f docker-compose.dev.yml ps"
echo "📋 View logs: docker-compose -f docker-compose.dev.yml logs -f"
