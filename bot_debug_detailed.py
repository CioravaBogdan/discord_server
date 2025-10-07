"""
Script de debugging pentru a verifica exact ce se întâmplă cu mesajele
"""

import discord
import requests
import json
import logging
from datetime import datetime
from config import Config

# Configurare logging FOARTE detaliat
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_debug.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Reducere logging pentru biblioteci externe
logging.getLogger('discord').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.WARNING)

class DebugBot:
    """Bot de debugging cu logging extins"""
    
    def __init__(self):
        logger.info("=" * 70)
        logger.info("🔍 PORNIRE BOT DE DEBUGGING")
        logger.info("=" * 70)
        
        # Verifică configurația
        try:
            Config.validate()
            logger.info(f"✅ Configurație validă")
            logger.info(f"   - Channel ID monitorizat: {Config.CHANNEL_ID}")
            logger.info(f"   - n8n webhook: {Config.N8N_WEBHOOK}")
        except Exception as e:
            logger.error(f"❌ Eroare configurație: {e}")
            raise
        
        # Setup Discord client
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        logger.info("🔧 Intents configurate:")
        logger.info(f"   - message_content: {intents.message_content}")
        logger.info(f"   - guilds: {intents.guilds}")
        logger.info(f"   - guild_messages: {intents.guild_messages}")
        
        self.client = discord.Client(intents=intents)
        self.setup_events()
        
        # Statistici
        self.stats = {
            'messages_received': 0,
            'messages_from_bots': 0,
            'messages_wrong_channel': 0,
            'messages_sent_to_n8n': 0,
            'n8n_success': 0,
            'n8n_errors': 0
        }
    
    def setup_events(self):
        """Setup Discord event handlers cu logging detaliat"""
        
        @self.client.event
        async def on_ready():
            logger.info("=" * 70)
            logger.info(f'✅ Bot conectat ca: {self.client.user.name} (ID: {self.client.user.id})')
            logger.info("=" * 70)
            
            # Afișează toate guild-urile (serverele)
            logger.info(f"📊 Servere conectate: {len(self.client.guilds)}")
            for guild in self.client.guilds:
                logger.info(f"   - {guild.name} (ID: {guild.id})")
                
                # Găsește canalul monitorizat
                channel = guild.get_channel(Config.CHANNEL_ID)
                if channel:
                    logger.info(f"   ✅ Canal monitorizat găsit: #{channel.name}")
                    logger.info(f"      Permisiuni bot:")
                    perms = channel.permissions_for(guild.me)
                    logger.info(f"      - Read Messages: {perms.read_messages}")
                    logger.info(f"      - Read Message History: {perms.read_message_history}")
                    logger.info(f"      - Send Messages: {perms.send_messages}")
        
        @self.client.event
        async def on_message(message):
            self.stats['messages_received'] += 1
            
            logger.info("=" * 70)
            logger.info(f"📨 MESAJ PRIMIT #{self.stats['messages_received']}")
            logger.info("=" * 70)
            logger.info(f"   Autor: {message.author.name} (ID: {message.author.id})")
            logger.info(f"   Este bot: {message.author.bot}")
            logger.info(f"   Canal: #{message.channel.name} (ID: {message.channel.id})")
            logger.info(f"   Content: {message.content[:100]}...")
            logger.info(f"   Attachments: {len(message.attachments)}")
            
            if message.attachments:
                for i, att in enumerate(message.attachments):
                    logger.info(f"      Attachment {i+1}: {att.filename} ({att.content_type})")
            
            # Verifică dacă este de la bot
            if message.author.bot:
                self.stats['messages_from_bots'] += 1
                logger.warning(f"⏭️  IGNORAT - Mesaj de la bot")
                logger.info(f"   Total mesaje ignorate (bot-uri): {self.stats['messages_from_bots']}")
                return
            
            # Verifică dacă este de la bot-ul însuși
            if message.author == self.client.user:
                logger.warning(f"⏭️  IGNORAT - Mesaj de la mine însuși")
                return
            
            # Verifică canalul
            if message.channel.id != Config.CHANNEL_ID:
                self.stats['messages_wrong_channel'] += 1
                logger.warning(f"⏭️  IGNORAT - Canal greșit")
                logger.info(f"   Canal așteptat: {Config.CHANNEL_ID}")
                logger.info(f"   Canal primit: {message.channel.id}")
                return
            
            logger.info("✅ MESAJ VALID - Pregătesc pentru trimitere la n8n")
            
            # Pregătește datele
            await self.send_to_n8n(message)
    
    async def send_to_n8n(self, message):
        """Trimite mesajul către n8n cu logging detaliat"""
        self.stats['messages_sent_to_n8n'] += 1
        
        # Pregătește payload-ul
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
                'is_bot': message.author.bot
            },
            'attachments': [],
            'guild': None
        }
        
        # Adaugă attachments
        if message.attachments:
            data['attachments'] = [
                {
                    'url': att.url,
                    'filename': att.filename,
                    'content_type': att.content_type,
                    'size': att.size
                } for att in message.attachments
            ]
            logger.info(f"📎 Adăugate {len(message.attachments)} attachments în payload")
        
        # Adaugă guild info
        if message.guild:
            data['guild'] = {
                'id': str(message.guild.id),
                'name': message.guild.name
            }
        
        # Log payload
        logger.info("📦 Payload n8n:")
        logger.info(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Trimite către n8n
        logger.info(f"🚀 Trimit către n8n: {Config.N8N_WEBHOOK}")
        
        try:
            response = requests.post(
                Config.N8N_WEBHOOK,
                json=data,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            logger.info(f"📡 Răspuns n8n:")
            logger.info(f"   Status Code: {response.status_code}")
            logger.info(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                self.stats['n8n_success'] += 1
                logger.info("✅ SUCCESS - Mesaj trimis cu succes către n8n")
                try:
                    response_data = response.json()
                    logger.info(f"   Răspuns JSON: {response_data}")
                except:
                    logger.info(f"   Răspuns text: {response.text[:200]}")
            elif response.status_code == 404:
                self.stats['n8n_errors'] += 1
                logger.error("❌ ERROR 404 - Webhook-ul n8n nu este activ sau URL incorect")
            else:
                self.stats['n8n_errors'] += 1
                logger.error(f"❌ ERROR {response.status_code}")
                logger.error(f"   Răspuns: {response.text}")
            
            # Afișează statistici
            self.print_stats()
                
        except requests.exceptions.Timeout:
            self.stats['n8n_errors'] += 1
            logger.error("❌ TIMEOUT - n8n nu răspunde în 10 secunde")
        except requests.exceptions.ConnectionError as e:
            self.stats['n8n_errors'] += 1
            logger.error(f"❌ CONNECTION ERROR - Nu pot conecta la n8n: {e}")
        except Exception as e:
            self.stats['n8n_errors'] += 1
            logger.error(f"❌ EROARE NEAȘTEPTATĂ: {e}", exc_info=True)
    
    def print_stats(self):
        """Afișează statisticile"""
        logger.info("")
        logger.info("📊 STATISTICI CURENTE:")
        logger.info(f"   Total mesaje primite: {self.stats['messages_received']}")
        logger.info(f"   Ignorate (bot-uri): {self.stats['messages_from_bots']}")
        logger.info(f"   Ignorate (canal greșit): {self.stats['messages_wrong_channel']}")
        logger.info(f"   Trimise către n8n: {self.stats['messages_sent_to_n8n']}")
        logger.info(f"   n8n SUCCESS: {self.stats['n8n_success']}")
        logger.info(f"   n8n ERRORS: {self.stats['n8n_errors']}")
        logger.info("")
    
    async def start(self):
        """Pornește bot-ul"""
        try:
            logger.info("🚀 Pornesc bot-ul Discord...")
            await self.client.start(Config.BOT_TOKEN)
        except discord.LoginFailure:
            logger.error("❌ Token Discord invalid!")
            raise
        except Exception as e:
            logger.error(f"❌ Eroare la pornirea bot-ului: {e}", exc_info=True)
            raise

if __name__ == "__main__":
    import asyncio
    
    bot = DebugBot()
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 70)
        logger.info("🛑 Bot oprit de utilizator")
        logger.info("=" * 70)
        bot.print_stats()
        logger.info("📄 Log complet salvat în: bot_debug.log")
    except Exception as e:
        logger.error(f"💥 Eroare critică: {e}", exc_info=True)
