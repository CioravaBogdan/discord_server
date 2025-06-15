import os
import sys
import asyncio
import discord
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Load environment variables
load_dotenv()

async def test_bot():
    """Test final pentru verificarea completă a bot-ului"""
    print("🔧 Test Final - Discord Bot cu n8n Integration")
    print("=" * 60)
    
    # 1. Verifică configurația
    print("\n1. Verificare configurație:")
    bot_token = os.getenv('BOT_TOKEN')
    channel_id = os.getenv('CHANNEL_ID')
    n8n_webhook = os.getenv('N8N_WEBHOOK')
    
    print(f"   ✅ Bot Token: {'Configurat' if bot_token else '❌ Lipsește'}")
    print(f"   ✅ Channel ID: {channel_id if channel_id else '❌ Lipsește'}")
    print(f"   ✅ n8n Webhook: {n8n_webhook if n8n_webhook else '❌ Lipsește'}")
    
    # 2. Test webhook server local
    print("\n2. Test webhook server local:")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Server activ: {data['status']}")
            print(f"   ✅ Bot Discord: {data['bot_status']}")
        else:
            print(f"   ❌ Server răspunde cu status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Server offline: {str(e)}")
    
    # 3. Test conexiune Discord
    print("\n3. Test conexiune Discord:")
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"   ✅ Bot conectat: {client.user}")
        
        # Verifică canalul
        channel = client.get_channel(int(channel_id))
        if channel:
            print(f"   ✅ Canal găsit: #{channel.name}")
            
            # Trimite mesaj de test
            try:
                await channel.send("🎉 **Test reușit!** Bot Discord conectat cu succes! Integrarea n8n este pregătită.")
                print(f"   ✅ Mesaj trimis în #{channel.name}")
            except Exception as e:
                print(f"   ❌ Nu pot trimite mesaj: {str(e)}")
        else:
            print(f"   ❌ Nu găsesc canalul cu ID: {channel_id}")
            
            # Afișează canalele disponibile
            for guild in client.guilds:
                print(f"\n   📋 Server: {guild.name}")
                for channel in guild.text_channels:
                    print(f"      📝 #{channel.name} (ID: {channel.id})")
        
        await client.close()
    
    try:
        await client.start(bot_token)
    except Exception as e:
        print(f"   ❌ Eroare conectare Discord: {str(e)}")
    
    # 4. Test webhook n8n
    print("\n4. Test webhook n8n:")
    test_data = {
        "content": "Test integrare Discord -> n8n",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message_id": f"test_{datetime.now().timestamp()}",
        "channel": {
            "id": channel_id,
            "name": "new-products"
        },
        "author": {
            "id": "bot_test",
            "username": "discord_bot_test",
            "display_name": "Bot Test"
        },
        "attachments": []
    }
    
    try:
        response = requests.post(n8n_webhook, json=test_data, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ n8n a primit datele cu succes!")
        elif response.status_code == 404:
            print(f"   ⚠️  Workflow-ul n8n nu este activ!")
            print(f"      Activează workflow-ul în n8n și încearcă din nou.")
        else:
            print(f"   ❌ n8n a răspuns cu status: {response.status_code}")
            print(f"      Răspuns: {response.text}")
    except Exception as e:
        print(f"   ❌ Eroare conectare n8n: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✨ Test complet finalizat!")
    print("\n📋 Următorii pași:")
    print("1. Verifică mesajul în canalul #new-products")
    print("2. Activează workflow-ul în n8n dacă nu este activ")
    print("3. Scrie un mesaj în Discord pentru a testa integrarea completă")

if __name__ == "__main__":
    asyncio.run(test_bot())
