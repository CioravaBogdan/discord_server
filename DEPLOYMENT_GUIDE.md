# Discord Bot Setup and Deployment Guide

## Overview
This Discord bot integrates with n8n workflows via webhooks. It:
- Listens for messages in specified Discord channels
- Sends Discord message data to n8n webhooks
- Receives webhooks from n8n to send messages/responses back to Discord
- Includes anti-loop protection to prevent message cycles
- Handles attachments and media files

## Prerequisites
- Python 3.8+
- Discord bot token
- n8n instance with webhook endpoints
- (Optional) Docker for containerized deployment

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
notepad .env  # or your preferred editor
```

Required values in `.env`:
- `BOT_TOKEN`: Your Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)
- `CHANNEL_ID`: The Discord channel ID where the bot should listen
- `N8N_WEBHOOK`: Your n8n webhook URL for receiving Discord messages

### 3. Run Tests
```bash
# Run all tests to verify setup
python -m pytest test_anti_loop.py test_filters.py -v

# Run individual test suites
python -m pytest test_anti_loop.py -v  # Anti-loop functionality
python -m pytest test_filters.py -v    # General filtering
```

### 4. Start the Bot
```bash
# Option 1: Run main application (recommended)
python main.py

# Option 2: Run bot and webhook server separately
python bot.py          # In one terminal
python webhook_server.py  # In another terminal
```

## Docker Deployment

### 1. Build and Run with Docker Compose
```bash
# Development mode
docker-compose -f docker-compose.dev.yml up --build

# Production mode
docker-compose up --build -d
```

### 2. View Logs
```bash
# View live logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f discord-bot
```

### 3. Rebuild After Code Changes
```bash
# Rebuild without cache
docker-compose build --no-cache
docker-compose up -d
```

## Bot Features

### Anti-Loop Protection
The bot includes sophisticated anti-loop protection to prevent message cycles:

- **🤖🔒 Prefix**: Messages with this prefix are automatically ignored
- **Bot Detection**: Automatically ignores messages from Discord bots
- **n8n Detection**: Recognizes and filters n8n-generated content
- **Duplicate Prevention**: Prevents processing of duplicate/repeated messages

### Message Filtering
The bot filters out:
- Bot messages (marked with `is_bot: true`)
- Known bot names (MEE6, Carl-bot, etc.)
- Messages with bot prefixes (🤖, 🚀, ⚡, etc.)
- n8n automation indicators
- System/webhook messages

### Webhook Integration
- **Incoming**: Receives Discord messages and sends to n8n
- **Outgoing**: Receives webhooks from n8n to send Discord messages
- **Health Check**: `/health` endpoint for monitoring
- **Anti-Loop Headers**: Recognizes `X-Source: n8n-automation` headers

## Configuration Options

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Discord bot token | - | ✅ |
| `CHANNEL_ID` | Discord channel ID to monitor | - | ✅ |
| `N8N_WEBHOOK` | n8n webhook URL | - | ✅ |
| `WEBHOOK_HOST` | Webhook server host | `0.0.0.0` | ❌ |
| `WEBHOOK_PORT` | Webhook server port | `8002` | ❌ |
| `LOG_LEVEL` | Logging level | `INFO` | ❌ |
| `DOCKER_ENV` | Docker mode flag | `false` | ❌ |
| `MAX_MESSAGE_CACHE` | Message cache size | `1000` | ❌ |

### Logging
- **Console**: Always enabled (important for Docker)
- **File**: Optional via `LOG_TO_FILE=true`
- **Levels**: DEBUG, INFO, WARNING, ERROR

## Testing

### Anti-Loop Tests
```bash
python -m pytest test_anti_loop.py -v
```
Tests the anti-loop functionality including:
- Prefix detection
- Bot message filtering
- Webhook simulation

### General Filter Tests
```bash
python -m pytest test_filters.py -v
```
Tests the general message filtering including:
- Normal user messages
- Bot detection
- n8n content recognition

### Manual Testing
1. Send a normal message in the Discord channel
2. Check logs to verify the message is processed
3. Send a message with 🤖 prefix
4. Verify it's filtered out

## Troubleshooting

### Common Issues

#### Bot Not Responding
1. Check bot token in `.env`
2. Verify bot has message content intent enabled
3. Ensure bot has permissions in the channel
4. Check logs for connection errors

#### Messages Not Reaching n8n
1. Verify `N8N_WEBHOOK` URL is correct
2. Check n8n webhook is active
3. Review network connectivity
4. Check for SSL/TLS issues

#### Docker Issues
1. Ensure `.env` file exists
2. Check Docker logs: `docker-compose logs -f`
3. Verify port mappings
4. Rebuild without cache: `docker-compose build --no-cache`

### Health Check
Visit `http://localhost:8002/health` to check bot status:
```json
{
  "status": "healthy",
  "bot_status": "connected",
  "webhook_port": 8002,
  "docker_mode": false
}
```

### Log Analysis
Check logs for these patterns:
- `✅ Procesez mesaj nou`: Message accepted for processing
- `🚫 Mesaj filtrat`: Message filtered out (anti-loop working)
- `✅ Mesaj trimis cu succes către n8n`: Successfully sent to n8n
- `❌ Eroare`: Error conditions

## Development

### Running in Development Mode
```bash
# Use development Docker compose
docker-compose -f docker-compose.dev.yml up

# Or run locally with debug logging
LOG_LEVEL=DEBUG python main.py
```

### Adding New Filters
1. Edit `message_filters.py`
2. Add new patterns to appropriate lists
3. Update tests in `test_filters.py`
4. Run tests to verify

### Code Structure
```
├── main.py              # Main application entry point
├── bot.py               # Discord bot implementation
├── webhook_server.py    # FastAPI webhook server
├── message_filters.py   # Anti-loop and message filtering
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── test_*.py           # Test files
├── docker-compose.yml  # Production Docker setup
└── .env.example        # Environment configuration template
```

## Security Notes

1. **Never commit `.env` file** - contains sensitive tokens
2. **Use secure webhooks** - HTTPS only for n8n endpoints
3. **Limit bot permissions** - only necessary Discord permissions
4. **Monitor logs** - check for suspicious activity
5. **Regular updates** - keep dependencies updated

## Support

For issues or questions:
1. Check the logs first
2. Run tests to verify functionality
3. Review this documentation
4. Check Discord bot permissions
5. Verify n8n webhook configuration
