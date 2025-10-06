#!/usr/bin/env python3
"""
Test complet pentru Discord Bot - verifică toate componentele
"""

import asyncio
import requests
import json
import sys
import os
from datetime import datetime
from config import Config, setup_logging

# Setup logging
logger = setup_logging()

def test_config():
    """Test 1: Verifică configurația"""
    print("🔧 Test 1: Verificare configurație...")
    try:
        Config.validate()
        print(f"✅ BOT_TOKEN: Configurat ({Config.BOT_TOKEN[:20]}...)")
        print(f"✅ CHANNEL_ID: {Config.CHANNEL_ID}")
        print(f"✅ N8N_WEBHOOK: {Config.N8N_WEBHOOK}")
        print(f"✅ WEBHOOK_PORT: {Config.WEBHOOK_PORT}")
        return True
    except Exception as e:
        print(f"❌ Eroare configurație: {e}")
        return False

def test_imports():
    """Test 2: Verifică importurile"""
    print("\n📦 Test 2: Verificare imports...")
    try:
        import discord
        print(f"✅ discord.py: {discord.__version__}")
        
        import requests
        print(f"✅ requests: {requests.__version__}")
        
        import fastapi
        print(f"✅ fastapi: {fastapi.__version__}")
        
        import uvicorn
        print(f"✅ uvicorn: {uvicorn.__version__}")
        
        from bot import DiscordBot
        print("✅ DiscordBot class importată cu succes")
        
        from webhook_server import app
        print("✅ Webhook server importat cu succes")
        
        return True
    except Exception as e:
        print(f"❌ Eroare import: {e}")
        return False

def test_webhook_connectivity():
    """Test 3: Verifică conectivitatea webhook-ului"""
    print("\n🌐 Test 3: Verificare conectivitate n8n webhook...")
    try:
        # Test simple ping către n8n
        test_data = {
            "test": True,
            "timestamp": datetime.now().isoformat(),
            "message": "Test conectivitate Discord Bot"
        }
        
        response = requests.post(
            Config.N8N_WEBHOOK,
            json=test_data,
            timeout=10,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'DiscordBot-Test/1.0'
            }
        )
        
        print(f"✅ Webhook răspunde cu status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Webhook funcționează perfect!")
            return True
        elif response.status_code == 404:
            print("⚠️ Webhook nu este activ (404) - verifică n8n workflow")
            return False
        else:
            print(f"⚠️ Status neașteptat: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - n8n nu răspunde în 10 secunde")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Nu pot conecta la n8n - verifică URL-ul")
        return False
    except Exception as e:
        print(f"❌ Eroare neașteptată: {e}")
        return False

def test_discord_token():
    """Test 4: Verifică validitatea token-ului Discord"""
    print("\n🤖 Test 4: Verificare token Discord...")
    try:
        import discord
        
        # Crează un client temporar pentru test
        intents = discord.Intents.default()
        intents.message_content = True
        
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ Bot conectat ca: {client.user.name} (ID: {client.user.id})")
            
            # Verifică canalul specificat
            channel = client.get_channel(Config.CHANNEL_ID)
            if channel:
                print(f"✅ Canal găsit: #{channel.name} în {channel.guild.name}")
            else:
                print(f"❌ Canalul cu ID {Config.CHANNEL_ID} nu a fost găsit")
            
            await client.close()
        
        # Test conexiune cu timeout
        print("   Conectez la Discord...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Rulează cu timeout de 15 secunde
        try:
            loop.run_until_complete(asyncio.wait_for(client.start(Config.BOT_TOKEN), timeout=15))
            return True
        except asyncio.TimeoutError:
            print("❌ Timeout la conectarea Discord (15s)")
            return False
        finally:
            if not client.is_closed():
                loop.run_until_complete(client.close())
            loop.close()
            
    except discord.LoginFailure:
        print("❌ Token Discord invalid!")
        return False
    except Exception as e:
        print(f"❌ Eroare Discord: {e}")
        return False

def test_directories():
    """Test 5: Verifică directoarele"""
    print("\n📁 Test 5: Verificare directoare...")
    try:
        # Verifică că directoarele există
        if Config.LOG_DIR.exists():
            print(f"✅ Director logs: {Config.LOG_DIR}")
        else:
            print(f"⚠️ Creez directorul logs: {Config.LOG_DIR}")
            Config.LOG_DIR.mkdir(exist_ok=True)
        
        if Config.DATA_DIR.exists():
            print(f"✅ Director data: {Config.DATA_DIR}")
        else:
            print(f"⚠️ Creez directorul data: {Config.DATA_DIR}")
            Config.DATA_DIR.mkdir(exist_ok=True)
        
        return True
    except Exception as e:
        print(f"❌ Eroare directoare: {e}")
        return False

def main():
    """Rulează toate testele"""
    print("=" * 60)
    print("🚀 DISCORD BOT - TEST COMPLET")
    print("=" * 60)
    
    tests = [
        ("Configurație", test_config),
        ("Imports", test_imports),
        ("Webhook n8n", test_webhook_connectivity),
        ("Token Discord", test_discord_token),
        ("Directoare", test_directories)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Eroare critică în testul {test_name}: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("📊 REZULTATE FINALE")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ TRECUT" if result else "❌ EȘUAT"
        print(f"{test_name:.<20} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"TOTAL: {passed}/{total} teste trecute")
    
    if passed == total:
        print("\n🎉 TOATE TESTELE AU TRECUT! Bot-ul este gata să ruleze!")
        print("\n🚀 Pentru a porni bot-ul:")
        print("   Local: python main.py")
        print("   Docker: docker-compose -f docker-compose-external.yml up -d")
        return True
    else:
        print(f"\n⚠️ {total - passed} teste au eșuat. Verifică erorile de mai sus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
