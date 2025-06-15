import asyncio
from config import Config, setup_logging
from bot import DiscordBot
import discord

# Setup logging
logger = setup_logging()

async def list_servers_and_channels():
    """List all servers and channels the bot can see"""
    try:
        Config.validate()
        
        # Setup Discord client
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f'Bot conectat ca {client.user}')
            print(f'Bot este pe {len(client.guilds)} servere:')
            print('=' * 50)
            
            for guild in client.guilds:
                print(f'📋 Server: {guild.name} (ID: {guild.id})')
                print(f'   Canale text:')
                
                for channel in guild.text_channels:
                    print(f'   📝 #{channel.name} (ID: {channel.id})')
                    if str(channel.id) == str(Config.CHANNEL_ID):
                        print(f'   ✅ ACESTA ESTE CANALUL MONITORIZAT!')
                
                print('-' * 30)
            
            print(f'\n🎯 Căutăm canalul cu ID: {Config.CHANNEL_ID}')
            target_channel = client.get_channel(Config.CHANNEL_ID)
            if target_channel:
                print(f'✅ Canalul găsit: #{target_channel.name} pe {target_channel.guild.name}')
            else:
                print(f'❌ Canalul cu ID {Config.CHANNEL_ID} nu a fost găsit!')
            
            await client.close()
        
        await client.start(Config.BOT_TOKEN)
        
    except Exception as e:
        logger.error(f"Eroare: {e}")

if __name__ == "__main__":
    asyncio.run(list_servers_and_channels())
