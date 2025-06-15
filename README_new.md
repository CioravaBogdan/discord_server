# Discord Bot cu Integrare n8n

Acest bot Discord permite integrarea cu n8n prin webhook-uri bidirectionale. Bot-ul poate trimite mesaje de pe Discord către n8n și poate primi comenzi de la n8n pentru a trimite mesaje înapoi în Discord.

## Caracteristici

- 🤖 Monitorizează mesajele dintr-un canal Discord specificat
- 🔗 Trimite datele mesajelor către webhook-uri n8n
- 📡 Primește webhook-uri de la n8n pentru a trimite mesaje în Discord
- 📎 Suportă atașamente și fișiere media
- ⚙️ Configurabil prin variabile de mediu
- 📝 Logging complet și gestionarea erorilor
- 🎨 Suport pentru Discord Embeds

## Tehnologii Utilizate

- **Python 3.8+**
- **discord.py** - Biblioteca Discord API
- **FastAPI** - Server webhook pentru primirea comenzilor de la n8n
- **requests** - Pentru trimiterea HTTP către n8n
- **uvicorn** - Server ASGI pentru FastAPI
- **python-dotenv** - Gestionarea variabilelor de mediu

## Instalare

### 1. Clonează/Descarcă proiectul

```bash
git clone <your-repo-url>
cd bot-discord
```

### 2. Instalează dependențele

```bash
pip install -r requirements.txt
```

### 3. Configurare

Editează fișierul `.env` și completează valorile:

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
