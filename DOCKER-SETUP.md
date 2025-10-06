# 🚀 Discord Bot + n8n - Setup Docker pe Windows 10

## Prerequisite

1. **Docker Desktop** pentru Windows instalat și funcțional
2. **PowerShell** (inclus în Windows 10)
3. **Git** (opțional, pentru clonarea repo-ului)

## Setup Rapid (5 minute)

### 1. Verifică Docker
```powershell
docker --version
docker compose version
```

### 2. Configurează aplicația
```powershell
# Clonează sau descarcă proiectul
cd "d:\Projects\BOT DISCORD"

# Verifică fișierul .env (ar trebui să existe deja)
notepad .env
```

### 3. Pornește aplicația
```powershell
# Rulează script-ul de setup
.\setup-docker.ps1
```

## Ce face script-ul de setup?

1. ✅ Verifică Docker și Docker Compose
2. ✅ Creează directoarele necesare (`logs/`, `data/`)
3. ✅ Construiește imaginile Docker
4. ✅ Pornește serviciile:
   - **n8n** pe portul `5678`
   - **Discord Bot** pe portul `8000`
   - **Redis** pe portul `6379`
5. ✅ Testează conectivitatea

## Servicii disponibile

| Serviciu | URL | Descriere |
|----------|-----|-----------|
| **n8n Web Interface** | http://localhost:5678 | Interface pentru workflow-uri |
| **Discord Bot API** | http://localhost:8000 | Webhook server pentru Discord |
| **Redis** | localhost:6379 | Cache și storage |

## Configurare n8n (După primul setup)

1. **Deschide n8n**: http://localhost:5678
2. **Creează workflow nou**
3. **Adaugă node "Webhook"**:
   - HTTP Method: `POST`
   - Path: `infant-discord-webhook`
   - URL completă: `http://localhost:5678/webhook/infant-discord-webhook`
4. **Salvează și ACTIVEAZĂ** workflow-ul

## Configurare Discord Channel ID

1. În Discord: **User Settings → Advanced → Developer Mode (ON)**
2. **Click dreapta** pe canalul dorit → **"Copy ID"**
3. **Editează .env**:
   ```
   CHANNEL_ID=YOUR_CHANNEL_ID_HERE
   ```
4. **Restart aplicația**:
   ```powershell
   docker compose restart discord-bot
   ```

## Comenzi utile

### Management containere
```powershell
# Vezi status
docker compose ps

# Vezi logs
docker compose logs -f

# Vezi logs doar pentru Discord bot
docker compose logs -f discord-bot

# Restart servicii
docker compose restart

# Oprește aplicația
.\stop-docker.ps1
```

### Debugging
```powershell
# Intră în containerul Discord bot
docker compose exec discord-bot bash

# Vezi logs n8n
docker compose logs -f n8n

# Testează webhook manual
curl -X POST "http://localhost:8000/send-message" -H "Content-Type: application/json" -d "{\"channel_id\": YOUR_CHANNEL_ID, \"content\": \"Test!\"}"
```

## Testare completă

### 1. Test n8n
- Deschide http://localhost:5678
- Ar trebui să vezi interfața n8n

### 2. Test Discord Bot
```powershell
# Test health check
curl http://localhost:8000/health

# Test webhook
curl -X POST "http://localhost:8000/send-message" -H "Content-Type: application/json" -d "{\"channel_id\": 1383864616052068414, \"content\": \"Test de la Docker!\"}"
```

### 3. Test integrare completă
1. Scrie un mesaj în canalul Discord monitorizat
2. Verifică logs-urile: `docker compose logs -f discord-bot`
3. Mesajul ar trebui să apară în n8n

## Troubleshooting

### Problem: Porturile sunt ocupate
```powershell
# Verifică ce rulează pe porturi
netstat -ano | findstr :5678
netstat -ano | findstr :8000
```

### Problem: Docker nu pornește
- Verifică Docker Desktop
- Restart Docker Desktop
- Verifică WSL2 (dacă este utilizat)

### Problem: Discord bot nu se conectează
- Verifică `BOT_TOKEN` în `.env`
- Verifică logs: `docker compose logs discord-bot`

### Problem: n8n nu răspunde
- Așteaptă 1-2 minute după primul start
- Verifică logs: `docker compose logs n8n`

## Structura fișierelor

```
BOT DISCORD/
├── docker-compose.yml     # Configurația serviciilor
├── Dockerfile            # Imaginea Discord bot
├── setup-docker.ps1      # Script de setup
├── stop-docker.ps1       # Script de oprire
├── .env                  # Configurația aplicației
├── logs/                 # Logs aplicației
├── data/                 # Date persistente
└── ... (cod aplicației)
```

## Update aplicația

```powershell
# Oprește aplicația
.\stop-docker.ps1

# Actualizează codul (dacă ai schimbări)
git pull

# Reconstruiește și pornește
.\setup-docker.ps1
```
