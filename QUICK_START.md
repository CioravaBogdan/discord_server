# Discord Bot cu n8n - Ghid Rapid de Configurare

## Pași Rapizi pentru Configurare:

### 1. Instalează dependențele
```bash
pip install -r requirements.txt
```

### 2. Configurează .env
Editează fișierul `.env` și completează:
- `N8N_WEBHOOK` - URL-ul webhook-ului tău n8n
- `CHANNEL_ID` - ID-ul canalului Discord pe care vrei să-l monitorizezi

Token-ul Discord este deja configurat.

### 3. Obține Channel ID
1. În Discord, mergi la User Settings > Advanced
2. Activează "Developer Mode"
3. Click dreapta pe canalul dorit
4. Selectează "Copy ID"
5. Pune ID-ul în `.env` la `CHANNEL_ID=`

### 4. Pornește bot-ul
```bash
python main.py
```
sau rulează `start_bot.bat`

## Testare Webhook
```bash
curl -X POST "http://localhost:8000/send-message" \
     -H "Content-Type: application/json" \
     -d '{"channel_id": YOUR_CHANNEL_ID, "content": "Test!"}'
```

## Endpoint-uri disponibile:
- `http://localhost:8000/` - Status
- `http://localhost:8000/health` - Health check  
- `http://localhost:8000/send-message` - Trimite mesaj în Discord
- `http://localhost:8000/webhook/n8n` - Webhook generic pentru n8n
