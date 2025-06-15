# 🚀 Primul Workflow n8n pentru Discord Bot

## Workflow 1: Monitorizare Mesaje Discord

### Pas 1: Creează Webhook în n8n

1. **Deschide n8n** în browser: `http://localhost:5678`
2. **Creează workflow nou**
3. **Adaugă node "Webhook"**:
   - HTTP Method: `POST`
   - Path: `discord-bot`
   - Response: `Immediately`
   - Full URL va fi: `http://localhost:5678/webhook/discord-bot`

### Pas 2: Procesare Date Discord

4. **Adaugă node "Code"** după Webhook:
```javascript
// Procesează datele primite de la Discord
const discordData = $input.all()[0].json;

// Log pentru debugging
console.log('Mesaj primit:', discordData.content);
console.log('De la:', discordData.author.username);

// Verifică cuvinte cheie
const keywords = ['help', 'urgent', 'problem', 'support'];
const needsAttention = keywords.some(keyword => 
  discordData.content.toLowerCase().includes(keyword)
);

// Verifică atașamente
const hasFiles = discordData.attachments && discordData.attachments.length > 0;

return [{
  json: {
    originalMessage: discordData,
    needsAttention: needsAttention,
    hasFiles: hasFiles,
    processedAt: new Date().toISOString(),
    summary: `${discordData.author.username}: ${discordData.content.substring(0, 50)}...`
  }
}];
```

### Pas 3: Răspuns Automat

5. **Adaugă node "IF"**:
   - Condition: `{{ $json.needsAttention }}` equals `true`

6. **Adaugă node "HTTP Request"** (pe ramura TRUE):
   - Method: `POST`
   - URL: `http://localhost:8000/send-message`
   - Headers: `Content-Type: application/json`
   - Body:
```json
{
  "channel_id": {{ $node["Webhook"].json["channel"]["id"] }},
  "content": "🤖 Am detectat că ai nevoie de ajutor! Cineva va răspunde în curând.",
  "embeds": [
    {
      "title": "Suport Automat",
      "description": "Mesajul tău a fost marcat ca prioritar",
      "color": 16776960,
      "fields": [
        {
          "name": "Mesaj Original",
          "value": "{{ $node[\"Webhook\"].json[\"content\"].substring(0, 100) }}...",
          "inline": false
        }
      ]
    }
  ]
}
```

### Pas 4: Salvare în Fișier (Opțional)

7. **Adaugă node "Write File"**:
   - File Path: `/tmp/discord_messages.json`
   - Data: `{{ JSON.stringify($node["Code"].json, null, 2) }}`

### Pas 5: Activează Workflow-ul

8. **Salvează și activează** workflow-ul în n8n

## Workflow 2: Notificări Programate

### Creează al doilea workflow pentru notificări automate:

1. **Node "Schedule Trigger"**:
   - Interval: `Every hour`

2. **Node "Code"**:
```javascript
const now = new Date();
const hour = now.getHours();

let message = "";
if (hour === 9) {
  message = "🌅 Bună dimineața! Să începem ziua!";
} else if (hour === 12) {
  message = "🍽️ E timpul pentru pauza de masă!";
} else if (hour === 17) {
  message = "🎯 Sfârșitul zilei de lucru se apropie!";
} else {
  return []; // Nu trimite mesaj
}

return [{
  json: {
    message: message,
    timestamp: now.toISOString()
  }
}];
```

3. **Node "HTTP Request"**:
   - Method: `POST`
   - URL: `http://localhost:8000/send-message`
   - Body:
```json
{
  "channel_id": YOUR_CHANNEL_ID,
  "content": "{{ $json.message }}"
}
```

## 🔧 Testing

### Test 1: Verifică Webhook
```bash
curl -X POST "http://localhost:5678/webhook/discord-bot" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "test urgent help",
       "channel": {"id": "123456789"},
       "author": {"username": "tester"}
     }'
```

### Test 2: Trimite Mesaj în Discord
```bash
curl -X POST "http://localhost:8000/send-message" \
     -H "Content-Type: application/json" \
     -d '{
       "channel_id": YOUR_CHANNEL_ID,
       "content": "Test din n8n!"
     }'
```

## 📝 Configurație Finală .env

```env
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
N8N_WEBHOOK=http://localhost:5678/webhook/discord-bot
CHANNEL_ID=YOUR_ACTUAL_CHANNEL_ID
WEBHOOK_HOST=0.0.0.0
WEBHOOK_PORT=8000
LOG_LEVEL=INFO
```

## 🚀 Pornire Finală

1. **Asigură-te că n8n rulează**
2. **Configurează workflow-urile în n8n**
3. **Actualizează CHANNEL_ID în .env**
4. **Pornește bot-ul**: `python main.py`

Gata! Bot-ul va trimite mesajele către n8n și va primi comenzi înapoi!
