# Copilot Instructions for Discord Bot with n8n Integration

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a Discord bot project that integrates with n8n workflows via webhooks. The bot should:

1. Listen for messages in specified Discord channels
2. Send Discord message data to n8n webhooks
3. Receive webhooks from n8n to send messages/responses back to Discord
4. Handle attachments and media files
5. Be configurable via environment variables
6. Include proper error handling and logging

Key technologies:
- Python 3.8+
- discord.py library
- requests library for HTTP
- FastAPI for webhook endpoints
- uvicorn for ASGI server
- python-dotenv for environment variables

The bot should be structured with:
- Main bot file (bot.py)
- Webhook server (webhook_server.py)
- Configuration management
- Proper logging
- Error handling
