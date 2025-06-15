# Discord Bot with n8n Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-blue.svg)](https://discordpy.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful Discord bot that integrates seamlessly with n8n workflows through bidirectional webhooks. Monitor Discord messages, trigger n8n workflows, and send automated responses back to Discord.

## 🌟 Features

- 🤖 **Discord Message Monitoring** - Automatically monitors specified Discord channels
- 🔗 **n8n Webhook Integration** - Sends Discord message data to n8n workflows
- 📡 **Bidirectional Communication** - Receives commands from n8n to send messages back to Discord
- 📎 **Rich Content Support** - Handles attachments, embeds, and media files
- ⚙️ **Environment Configuration** - Easy setup through environment variables
- 📝 **Comprehensive Logging** - Detailed logging and error handling
- 🎨 **Discord Embeds** - Full support for rich Discord embeds
- 🚀 **Production Ready** - Robust error handling and reconnection logic

## 🛠️ Technologies

- **Python 3.8+**
- **discord.py** - Discord API library
- **FastAPI** - Modern web framework for webhook server
- **uvicorn** - ASGI server for FastAPI
- **requests** - HTTP library for n8n communication
- **python-dotenv** - Environment variables management

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- n8n instance (local or cloud)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/CioravaBogdan/discord_server.git
   cd discord_server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Copy `.env.example` to `.env` and fill in your values:
   ```env
   BOT_TOKEN=your_discord_bot_token
   N8N_WEBHOOK=https://your-n8n-instance.com/webhook/discord-bot
   CHANNEL_ID=your_discord_channel_id
   WEBHOOK_PORT=8000
   LOG_LEVEL=INFO
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

```env
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
N8N_WEBHOOK=YOUR_N8N_WEBHOOK_URL
CHANNEL_ID=YOUR_DISCORD_CHANNEL_ID
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
LOG_LEVEL=INFO
```

### 4. Obținerea Token-ului Discord

Token-ul furnizat este:
```
YOUR_DISCORD_BOT_TOKEN_HERE
```

### 5. Obținerea Channel ID

1. Activează "Developer Mode" în Discord (User Settings > Advanced)
2. Click dreapta pe canalul dorit
3. Selectează "Copy ID"

## Utilizare

### Rularea Bot-ului

```bash
python main.py
```

Aceasta va porni atât bot-ul Discord cât și serverul webhook.

### Rularea Separată

Pentru a rula doar bot-ul Discord:
```bash
python bot.py
```

Pentru a rula doar serverul webhook:
```bash
python webhook_server.py
```

## Integrare cu n8n

### 1. Primirea Mesajelor de la Discord

Bot-ul trimite automat mesajele către webhook-ul n8n configurat. Structura datelor trimise:

```json
{
  "content": "Conținutul mesajului",
  "timestamp": "2025-06-15T10:30:00.000Z",
  "message_id": "123456789",
  "channel": {
    "id": "123456789",
    "name": "general"
  },
  "author": {
    "id": "987654321",
    "username": "utilizator",
    "display_name": "Nume Afișat",
    "avatar_url": "https://cdn.discordapp.com/avatars/..."
  },
  "guild": {
    "id": "555666777",
    "name": "Server Name"
  },
  "attachments": [
    {
      "url": "https://cdn.discordapp.com/attachments/...",
      "filename": "image.png",
      "content_type": "image/png",
      "size": 1024000,
      "spoiler": false
    }
  ]
}
```

### 2. Trimiterea Mesajelor către Discord

Pentru a trimite mesaje din n8n către Discord, fă un HTTP POST către:

**URL:** `http://localhost:8000/send-message`

**Body:**
```json
{
  "channel_id": 123456789012345678,
  "content": "Mesajul tău aici",
  "embeds": [
    {
      "title": "Titlu Embed",
      "description": "Descrierea embed-ului",
      "color": 16711680,
      "fields": [
        {
          "name": "Câmp 1",
          "value": "Valoare 1",
          "inline": true
        }
      ]
    }
  ]
}
```

### 3. Webhook Generic n8n

Pentru integrări mai complexe, poți folosi endpoint-ul generic:

**URL:** `http://localhost:8000/webhook/n8n`

**Body:**
```json
{
  "action": "send_message",
  "channel_id": 123456789012345678,
  "content": "Mesaj din n8n",
  "embeds": []
}
```

## Endpoint-uri API

### GET `/`
Verificarea stării serverului

### GET `/health`
Verificare detaliată a stării (bot + webhook server)

### POST `/send-message`
Trimite un mesaj în Discord

### POST `/webhook/n8n`
Endpoint generic pentru n8n

## Configurare Rapidă

1. Editează `.env` cu token-ul și webhook-ul tău n8n
2. Rulează `pip install -r requirements.txt`
3. Rulează `python main.py`
4. Bot-ul va fi activ pe portul 8000 pentru webhook-uri

## Exemplu de Test

Pentru a testa webhook-ul, folosește:

```bash
curl -X POST "http://localhost:8000/send-message" \
     -H "Content-Type: application/json" \
     -d '{
       "channel_id": YOUR_CHANNEL_ID,
       "content": "Test message from n8n!"
     }'
```

## Token Discord

Token-ul furnizat este pentru bot-ul `infant_products` (ID: 1383874977777979544):
```
YOUR_DISCORD_BOT_TOKEN_HERE
```

## Depanare

- Verifică că `.env` conține valorile corecte
- Asigură-te că bot-ul are permisiunile necesare în server
- Verifică logs-urile pentru erori de conectare
- Testează endpoint-urile cu curl sau Postman

Pentru debugging mai detaliat:
```env
LOG_LEVEL=DEBUG
```

## 🐳 Lucru cu n8n în Docker (Existent)

Dacă ai deja n8n rulând în Docker, configurația este foarte simplă:

### 1. Verifică că n8n rulează
```bash
# Verifică containerele Docker
docker ps | grep n8n

# Sau testează accesul
curl http://localhost:5678
```

### 2. Configurează webhook-ul în .env
```env
# URL-ul către n8n Docker (portul standard este 5678)
N8N_WEBHOOK=http://localhost:5678/webhook/discord-bot
```

### 3. Creează primul workflow în n8n
- Deschide n8n: `http://localhost:5678`
- Urmează ghidul din `first_workflow.md`
- Webhook path: `discord-bot`

### 4. Testează integrarea
```bash
# Test rapid conexiune
python test_connection.py

# Sau cu batch file
test_setup.bat
```

## 📁 Fișiere Helper Create

- **`first_workflow.md`** - Ghid pas cu pas pentru primul workflow n8n
- **`n8n_setup.md`** - Configurație detaliată n8n 
- **`test_connection.py`** - Script Python pentru testare
- **`test_setup.bat`** - Script Windows pentru verificare rapidă
- **`docker_setup.md`** - Opțiuni Docker complete
