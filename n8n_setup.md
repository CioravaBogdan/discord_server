# Configurare n8n pentru Discord Bot

## 📋 Configurare Webhook-uri în n8n

### 1. Webhook pentru Primirea Mesajelor de la Discord

În n8n, creează un workflow nou cu următoarele noduri:

#### Node 1: Webhook (Trigger)
- **Method**: POST
- **Path**: `discord-bot`
- **Response Mode**: Immediately
- **URL completă**: `http://localhost:5678/webhook/discord-bot`

#### Node 2: Code (Optional - pentru procesare)
```javascript
// Procesează datele primite de la Discord
const discordData = $input.all()[0].json;

// Extrage informațiile importante
const message = {
  content: discordData.content,
  author: discordData.author.username,
  channel: discordData.channel.name,
  timestamp: discordData.timestamp,
  hasAttachments: discordData.attachments.length > 0
};

// Verifică dacă mesajul conține cuvinte cheie
const keywords = ['urgent', 'help', 'problem', 'bug'];
const isImportant = keywords.some(keyword => 
  discordData.content.toLowerCase().includes(keyword)
);

return [{
  json: {
    ...message,
    isImportant: isImportant,
    originalData: discordData
  }
}];
```

#### Node 3: IF (Conditional)
- **Condition**: `{{ $json.isImportant }}` equals `true`

#### Node 4: HTTP Request (pentru răspuns automat)
- **Method**: POST
- **URL**: `http://localhost:8000/send-message`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "channel_id": {{ $node["Webhook"].json["channel"]["id"] }},
  "content": "Mesaj important detectat! Voi verifica în curând.",
  "embeds": [
    {
      "title": "Notificare Automată",
      "description": "Am primit mesajul tău și îl voi procesa.",
      "color": 3447003
    }
  ]
}
```

### 2. Workflow pentru Trimiterea Mesajelor către Discord

#### Node 1: Manual Trigger sau Schedule
Pentru testare sau automatizare

#### Node 2: Set (pentru pregătirea datelor)
```json
{
  "channel_id": 123456789012345678,
  "content": "Mesaj automat de la n8n!",
  "embeds": [
    {
      "title": "Status Update",
      "description": "Toate sistemele funcționează normal",
      "color": 65280,
      "timestamp": "{{ $now.toISOString() }}"
    }
  ]
}
```

#### Node 3: HTTP Request
- **Method**: POST
- **URL**: `http://localhost:8000/send-message`
- **Headers**: `Content-Type: application/json`
- **Body**: `{{ $json }}`

### 3. Workflow Avansat: Monitorizare și Alertă

#### Pentru monitorizarea sistemelor și trimiterea de alerte în Discord:

```javascript
// Node Code pentru verificarea statusului
const services = [
  { name: 'Database', url: 'http://localhost:5432' },
  { name: 'API', url: 'http://localhost:3000/health' },
  { name: 'Cache', url: 'http://localhost:6379' }
];

// Simulează verificarea serviciilor
const results = services.map(service => ({
  name: service.name,
  status: Math.random() > 0.1 ? 'online' : 'offline',
  responseTime: Math.floor(Math.random() * 1000)
}));

const offlineServices = results.filter(r => r.status === 'offline');

return [{
  json: {
    services: results,
    hasIssues: offlineServices.length > 0,
    offlineServices: offlineServices
  }
}];
```

## 🔗 URL-uri Important pentru Configurare

### Din n8n către Discord Bot:
- **Webhook Discord Bot**: `http://localhost:8000/send-message`
- **Webhook Generic**: `http://localhost:8000/webhook/n8n`
- **Health Check**: `http://localhost:8000/health`

### Din Discord Bot către n8n:
- **Webhook n8n**: `http://localhost:5678/webhook/discord-bot`

## ⚙️ Configurare .env

Actualizează fișierul `.env` cu:

```env
# URL către n8n (portul standard Docker n8n este 5678)
N8N_WEBHOOK=http://localhost:5678/webhook/discord-bot

# ID-ul canalului Discord (click dreapta pe canal → Copy ID)
CHANNEL_ID=your_actual_channel_id

# Portul pentru webhook server (8000 e ok dacă nu e folosit)
WEBHOOK_PORT=8000
```

## 🧪 Testare Configurație

### Test 1: Verifică că n8n primește date de la Discord
1. Pornește bot-ul Discord: `python main.py`
2. Scrie un mesaj în canalul monitorizat
3. Verifică în n8n că webhook-ul a primit datele

### Test 2: Verifică că Discord primește mesaje de la n8n
```bash
curl -X POST "http://localhost:8000/send-message" \
     -H "Content-Type: application/json" \
     -d '{
       "channel_id": YOUR_CHANNEL_ID,
       "content": "Test din n8n!"
     }'
```

### Test 3: Workflow complet
1. Activează workflow-ul în n8n
2. Scrie un mesaj cu cuvântul "urgent" în Discord
3. Verifică că bot-ul răspunde automat

## 🔧 Depanare

### Dacă n8n nu primește mesaje:
- Verifică că `N8N_WEBHOOK` din `.env` e corect
- Verifică că workflow-ul din n8n e activat
- Verifică logs-urile bot-ului pentru erori de conexiune

### Dacă Discord nu primește mesaje:
- Verifică că bot-ul rulează pe portul 8000
- Verifică că `CHANNEL_ID` e corect în `.env`
- Testează endpoint-ul manual cu curl

### Logs utile:
```bash
# Activează logging detaliat
LOG_LEVEL=DEBUG
```
