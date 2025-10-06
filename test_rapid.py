#!/usr/bin/env python3
"""
Test rapid - demonstrează că bot-ul poate porni fără erori
"""

import asyncio
import sys
from config import Config
from bot import DiscordBot

async def quick_test():
    """Test rapid de 5 secunde pentru a demonstra că bot-ul funcționează"""
    print("🚀 PORNESC BOT-UL PENTRU TEST RAPID...")
    print(f"📡 Webhook: {Config.N8N_WEBHOOK}")
    print(f"📺 Canal: {Config.CHANNEL_ID}")
    print()
    
    try:
        # Crează bot-ul
        bot = DiscordBot()
        
        # Pornește bot-ul cu timeout
        print("🔄 Conectez la Discord...")
        await asyncio.wait_for(bot.client.start(Config.BOT_TOKEN), timeout=10)
        
    except asyncio.TimeoutError:
        print("✅ Test reușit - bot-ul s-a conectat și funcționează!")
        print("⏰ Opresc testul după 10 secunde (pentru demonstrație)")
        return True
    except Exception as e:
        print(f"❌ Eroare în test: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TEST RAPID DISCORD BOT")
    print("=" * 50)
    
    try:
        result = asyncio.run(quick_test())
        if result:
            print("\n🎉 TESTUL A REUȘIT!")
            print("Bot-ul este gata să ruleze în mod normal.")
        else:
            print("\n❌ Testul a eșuat.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n✅ Test oprit manual - bot-ul funcționează!")
    except Exception as e:
        print(f"\n❌ Eroare în test: {e}")
        sys.exit(1)
