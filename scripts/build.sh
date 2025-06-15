#!/bin/bash
set -e

echo "🔨 Building Discord Bot Docker images..."

# Build production image
echo "📦 Building production image..."
docker build -t infant-discord-bot:latest .

# Build development image
echo "🛠️ Building development image..."
docker build -f Dockerfile.dev -t infant-discord-bot:dev .

echo "✅ Docker images built successfully!"
echo ""
echo "🐳 Available images:"
docker images | grep "infant-discord-bot"
