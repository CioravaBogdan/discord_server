FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash discord-bot \
    && chown -R discord-bot:discord-bot /app

# Create directories for logs and data
RUN mkdir -p /app/logs /app/data \
    && chown -R discord-bot:discord-bot /app/logs /app/data

USER discord-bot

# Health check - using different port to avoid conflicts
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Expose webhook port (8002 to avoid conflicts)
EXPOSE 8002

# Set environment variable for Docker
ENV DOCKER_ENV=true

# Run the application
CMD ["python", "main.py"]
