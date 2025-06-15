import discord
import requests
import json
import logging
import asyncio
from typing import Dict, Any
from config import Config, setup_logging

# Setup logging
logger = setup_logging()

class DiscordBot:
    """Discord bot that integrates with n8n via webhooks"""
    
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Setup Discord client with proper intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        self.client = discord.Client(intents=intents)
        self.setup_events()
        
    def setup_events(self):
        """Setup Discord event handlers"""
        
        @self.client.event
        async def on_ready():
            logger.info(f'Bot conectat ca {self.client.user}')
            logger.info(f'Monitorizez canalul cu ID: {Config.CHANNEL_ID}')
        
        @self.client.event
        async def on_message(message):
            await self.handle_message(message)
    
    async def handle_message(self, message: discord.Message):
        """Handle incoming Discord messages"""
        # Skip messages from the bot itself
        if message.author == self.client.user:
            return
            
        # Check if message is in the monitored channel
        if message.channel.id != Config.CHANNEL_ID:
            return
            
        logger.info(f"Mesaj nou de la {message.author.name}: {message.content[:50]}...")
        
        # Prepare message data for n8n
        message_data = await self.prepare_message_data(message)
        
        # Send to n8n webhook
        await self.send_to_n8n(message_data)
    
    async def prepare_message_data(self, message: discord.Message) -> Dict[str, Any]:
        """Prepare message data for n8n webhook"""
        data = {
            'content': message.content,
            'timestamp': message.created_at.isoformat(),
            'message_id': str(message.id),
            'channel': {
                'id': str(message.channel.id),
                'name': message.channel.name
            },
            'author': {
                'id': str(message.author.id),
                'username': message.author.name,
                'display_name': message.author.display_name,
                'avatar_url': str(message.author.avatar.url) if message.author.avatar else None
            },
            'guild': {
                'id': str(message.guild.id),
                'name': message.guild.name
            } if message.guild else None,
            'attachments': []
        }
        
        # Process attachments
        for attachment in message.attachments:
            attachment_data = {
                'url': attachment.url,
                'filename': attachment.filename,
                'content_type': attachment.content_type,
                'size': attachment.size,
                'spoiler': attachment.is_spoiler()
            }
            data['attachments'].append(attachment_data)
        
        return data
    
    async def send_to_n8n(self, data: Dict[str, Any]):
        """Send data to n8n webhook"""
        try:
            response = requests.post(
                Config.N8N_WEBHOOK,
                json=data,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                logger.info(f"Trimis cu succes la n8n: {response.status_code}")
            else:
                logger.warning(f"Răspuns neașteptat de la n8n: {response.status_code}")
                logger.warning(f"Răspuns: {response.text}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Eroare la trimiterea către n8n: {e}")
        except Exception as e:
            logger.error(f"Eroare neașteptată: {e}")
    
    async def send_discord_message(self, channel_id: int, content: str, embeds: list = None):
        """Send a message to Discord (used by webhook server)"""
        try:
            channel = self.client.get_channel(channel_id)
            if not channel:
                logger.error(f"Canal cu ID {channel_id} nu a fost găsit")
                return False
                
            await channel.send(content=content, embeds=embeds)
            logger.info(f"Mesaj trimis în canalul {channel.name}")
            return True
            
        except Exception as e:
            logger.error(f"Eroare la trimiterea mesajului Discord: {e}")
            return False
    
    def run(self):
        """Start the Discord bot"""
        logger.info("Pornesc bot-ul Discord...")
        self.client.run(Config.BOT_TOKEN)

# Global bot instance for webhook server
bot_instance = None

def get_bot_instance():
    """Get the global bot instance"""
    return bot_instance

if __name__ == "__main__":
    bot = DiscordBot()
    bot_instance = bot
    bot.run()
