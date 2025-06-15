# Docker Setup pentru Discord Bot + n8n (Opțional)

În cazul în care vrei să rulezi bot-ul Discord într-un container Docker alături de n8n:

## docker-compose.yml (pentru setup complet)

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - discord_network

  discord-bot:
    build: .
    container_name: discord-bot
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - N8N_WEBHOOK=http://n8n:5678/webhook/discord-bot
      - CHANNEL_ID=${CHANNEL_ID}
      - WEBHOOK_HOST=0.0.0.0
      - WEBHOOK_PORT=8000
    depends_on:
      - n8n
    networks:
      - discord_network

volumes:
  n8n_data:

networks:
  discord_network:
    driver: bridge
```

## Dockerfile pentru bot

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

## Setup rapid

```bash
# Dacă vrei să rulezi totul în Docker
docker-compose up -d

# Sau doar n8n în Docker și bot-ul local
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# Apoi bot-ul local
python main.py
```

## Configurare Recomandată (n8n în Docker, bot local)

1. **n8n în Docker** (dacă nu îl ai deja):
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=password \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

2. **Bot Discord local**:
```bash
pip install -r requirements.txt
python main.py
```

## Avantaje Setup Mixt:
- n8n persistent în Docker
- Bot ușor de debugat local
- Acces rapid la logs
- Dezvoltare mai rapidă
