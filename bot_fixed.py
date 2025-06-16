import discord
import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any
from config import Config

# Configurare logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DiscordBot:
    """Discord bot for message monitoring and n8n webhook integration"""
    
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
        # ⭐ SOLUȚIA PRINCIPALĂ - Ignoră mesajele de la bot-uri
        if message.author.bot:
            logger.debug(f"Ignorat mesaj de la bot: {message.author.name}")
            return
            
        # Skip messages from the bot itself (redundant but safe)
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
                'display_name': message.author.display_name or message.author.name,
                'is_bot': message.author.bot  # ⭐ Adaugă flag pentru bot
            },
            'attachments': [],
            'guild': None
        }
        
        # Add attachments if present
        if message.attachments:
            data['attachments'] = [
                {
                    'url': att.url,
                    'filename': att.filename,
                    'content_type': att.content_type,
                    'size': att.size
                } for att in message.attachments
            ]
        
        # Add guild info if available
        if message.guild:
            data['guild'] = {
                'id': str(message.guild.id),
                'name': message.guild.name
            }
        
        return data
    
    async def send_to_n8n(self, data: Dict[str, Any]):
        """Send data to n8n webhook"""
        try:
            response = requests.post(
                Config.N8N_WEBHOOK,
                json=data,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                logger.info("✅ Mesaj trimis cu succes către n8n")
            elif response.status_code == 404:
                logger.warning("⚠️ Webhook-ul n8n nu este activ sau URL incorect")
            else:
                logger.error(f"❌ n8n a răspuns cu status {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            logger.error("❌ Timeout la trimiterea către n8n (>10s)")
        except requests.exceptions.ConnectionError:
            logger.error("❌ Nu pot conecta la n8n - verifică dacă n8n rulează")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Eroare la trimiterea către n8n: {str(e)}")
    
    async def send_discord_message(self, channel_id: int, content: str, embed_data: Dict[str, Any] = None) -> bool:
        """Send message to Discord channel"""
        try:
            channel = self.client.get_channel(channel_id)
            if not channel:
                logger.error(f"Nu găsesc canalul cu ID: {channel_id}")
                return False
            
            # ⭐ Adaugă prefix pentru mesajele de la n8n pentru a le identifica
            if not content.startswith("🤖"):
                content = f"🤖 {content}"
            
            if embed_data:
                embed = discord.Embed(**embed_data)
                await channel.send(content=content, embed=embed)
            else:
                await channel.send(content)
                
            logger.info(f"✅ Mesaj trimis în #{channel.name}")
            return True
            
        except discord.Forbidden:
            logger.error(f"❌ Nu am permisiuni să trimit mesaje în canalul {channel_id}")
            return False
        except discord.HTTPException as e:
            logger.error(f"❌ Eroare HTTP Discord: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Eroare neașteptată: {str(e)}")
            return False
    
    async def start(self):
        """Start the Discord bot"""
        try:
            logger.info("🚀 Pornesc Discord bot...")
            await self.client.start(Config.BOT_TOKEN)
        except discord.LoginFailure:
            logger.error("❌ Token Discord invalid")
            raise
        except Exception as e:
            logger.error(f"❌ Eroare la pornirea bot-ului: {str(e)}")
            raise

if __name__ == "__main__":
    import asyncio
    
    bot = DiscordBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 Bot oprit de utilizator")
    except Exception as e:
        logger.error(f"💥 Eroare critică: {str(e)}")
