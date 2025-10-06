# 🚀 GHID COMPLET - Discord Bot + n8n în Docker pe Windows 10

## ⚡ SETUP RAPID (5 MINUTE)

### 1. Verifică prerequisite
```powershell
# Verifică Docker
docker --version
docker compose version

# Verifică PowerShell
$PSVersionTable.PSVersion
```

### 2. Setup cu un singur script
```powershell
# Navighează în folderul proiectului
cd "d:\Projects\BOT DISCORD"

# Rulează setup-ul automat
.\setup-docker.ps1
```

### 3. Testează aplicația
```powershell
# Rulează testele automate
.\test-docker.ps1
```

## 🎯 CE FACE SETUP-UL AUTOMAT

1. ✅ **Verifică Docker** și dependențele
2. ✅ **Creează directoare** necesare (`logs/`, `data/`)
3. ✅ **Construiește imaginile** Docker
4. ✅ **Pornește serviciile**:
   - **n8n**: http://localhost:5678
   - **Discord Bot**: http://localhost:8000
   - **Redis**: localhost:6379
5. ✅ **Testează conectivitatea**
6. ✅ **Afișează logs live**

## 📋 SERVICII ACTIVE

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| **n8n** | http://localhost:5678 | Interface web pentru workflow-uri |
| **Discord Bot API** | http://localhost:8000 | Webhook server |
| **Redis** | localhost:6379 | Cache și storage |

## 🔧 CONFIGURARE n8n (PRIMUL RUN)

### Pas 1: Deschide n8n
- URL: http://localhost:5678
- Prima dată va trebui să faci setup-ul inițial

### Pas 2: Creează workflow pentru Discord
1. **New Workflow**
2. **Add Node** → **Trigger** → **Webhook**
3. **Configurează webhook**:
   - HTTP Method: `POST`
   - Path: `infant-discord-webhook`
   - Response: `Immediately`
4. **ACTIVEAZĂ** workflow-ul (butonul din dreapta sus)

### Pas 3: URL-ul webhook va fi:
```
http://localhost:5678/webhook/infant-discord-webhook
```

## 📱 CONFIGURARE DISCORD

### 1. Obține Channel ID
1. Discord → **User Settings** → **Advanced** → **Developer Mode (ON)**
2. **Click dreapta** pe canalul dorit → **"Copy ID"**
3. Editează `.env`:
   ```
   CHANNEL_ID=YOUR_CHANNEL_ID_HERE
   ```

### 2. Restart Discord Bot
```powershell
docker compose restart discord-bot
```

## 🧪 TESTARE COMPLETĂ

### Test 1: Servicii active
```powershell
docker compose ps
```

### Test 2: n8n Web Interface
- Deschide: http://localhost:5678
- Ar trebui să vezi interfața n8n

### Test 3: Discord Bot Health
```powershell
curl http://localhost:8000/health
```

### Test 4: Webhook manual
```powershell
curl -X POST "http://localhost:8000/send-message" `
     -H "Content-Type: application/json" `
     -d '{"channel_id": YOUR_CHANNEL_ID, "content": "Test din Docker!"}'
```

### Test 5: Integrare completă
1. Scrie un mesaj în canalul Discord monitorizat
2. Verifică logs: `docker compose logs -f discord-bot`
3. Mesajul ar trebui să apară în n8n

## 📊 MANAGEMENT APLICAȚIE

### Comenzi de bază
```powershell
# Status servicii
docker compose ps

# Logs toate serviciile
docker compose logs -f

# Logs doar Discord bot
docker compose logs -f discord-bot

# Logs n8n
docker compose logs -f n8n

# Restart toate serviciile
docker compose restart

# Restart doar Discord bot
docker compose restart discord-bot

# Oprește aplicația
.\stop-docker.ps1
```

### Debugging
```powershell
# Intră în containerul Discord bot
docker compose exec discord-bot bash

# Verifică variabilele de environment
docker compose exec discord-bot env | grep -E "(BOT_TOKEN|CHANNEL_ID|N8N_WEBHOOK)"

# Testează conectivitatea internă
docker compose exec discord-bot curl http://n8n:5678
```

## 🔍 TROUBLESHOOTING

### Problem: "Port already in use"
```powershell
# Verifică ce folosește porturile
netstat -ano | findstr :5678
netstat -ano | findstr :8000

# Oprește procesele care blochează
taskkill /PID <PID_NUMBER> /F
```

### Problem: Docker Desktop nu pornește
1. **Restart Docker Desktop**
2. Verifică **WSL2** (dacă este activat)
3. Restart Windows (dacă e necesar)

### Problem: Discord bot nu se conectează
```powershell
# Verifică logs
docker compose logs discord-bot

# Verifică token-ul în .env
notepad .env
```

### Problem: n8n nu răspunde
1. **Așteaptă 1-2 minute** după primul start
2. Verifică logs: `docker compose logs n8n`
3. Verifică dacă portul 5678 este liber

## 📁 STRUCTURA DOCKER

```
BOT DISCORD/
├── 🐳 docker-compose.yml    # Configurația serviciilor
├── 🐳 Dockerfile           # Imaginea Discord bot
├── ⚡ setup-docker.ps1     # Setup automat
├── 🛑 stop-docker.ps1      # Oprire aplicație
├── 🧪 test-docker.ps1      # Teste automate
├── 📖 DOCKER-SETUP.md      # Acest ghid
├── 🔧 .env                 # Configurația aplicației
├── 📁 logs/                # Logs aplicației (Docker volume)
├── 📁 data/                # Date persistente (Docker volume)
└── 🐍 (cod Python)         # Codul aplicației
```

## 🔄 UPDATE APLICAȚIEI

```powershell
# Oprește aplicația
.\stop-docker.ps1

# Actualizează codul (dacă ai modificări)
# git pull  # sau copiază fișierele noi

# Reconstruiește și pornește
.\setup-docker.ps1
```

## 🎉 READY TO USE!

După ce ai rulat `.\setup-docker.ps1` și testele trec, aplicația ta este **gata de utilizare**!

### Quick Start:
1. ✅ **n8n**: http://localhost:5678 → Creează workflow cu webhook
2. ✅ **Discord**: Scrie în canalul monitorizat
3. ✅ **Logs**: `docker compose logs -f` pentru monitoring

### Support:
- **Logs**: `docker compose logs -f`
- **Status**: `docker compose ps`
- **Test**: `.\test-docker.ps1`
