"""
Script pentru testare live a bot-ului Discord
Pornește bot-ul și monitorizează pentru 30 secunde dacă primește mesaje
"""

import asyncio
import logging
import sys
from datetime import datetime
from bot import DiscordBot

# Configurare logging cu mai multe detalii
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BotLiveTester:
    """Testează bot-ul în mod live"""
    
    def __init__(self):
        self.bot = None
        self.messages_received = 0
        self.messages_sent_to_n8n = 0
        self.messages_ignored = 0
    
    async def run_test(self, duration=30):
        """Rulează bot-ul pentru o perioadă de timp"""
        print("\n" + "=" * 70)
        print("🧪 TESTARE LIVE BOT DISCORD")
        print("=" * 70)
        print(f"\n⏱️  Bot-ul va rula pentru {duration} secunde")
        print("📝 Trimite un mesaj în canalul monitorizat pentru a testa")
        print("🛑 Apasă Ctrl+C pentru a opri testul mai devreme\n")
        print("=" * 70)
        
        # Creează bot-ul
        self.bot = DiscordBot()
        
        # Interceptează metoda handle_message pentru statistici
        original_handle = self.bot.handle_message
        
        async def tracked_handle_message(message):
            self.messages_received += 1
            
            # Verifică dacă va fi ignorat
            if message.author.bot:
                self.messages_ignored += 1
                logger.info(f"📊 Mesaj ignorat (de la bot): {message.author.name}")
            elif message.channel.id != self.bot.client.guilds[0].channels[0].id if self.bot.client.guilds else None:
                logger.debug(f"📊 Mesaj din alt canal: {message.channel.name}")
            else:
                self.messages_sent_to_n8n += 1
                logger.info(f"📊 Mesaj procesat și trimis către n8n")
            
            # Apelează funcția originală
            await original_handle(message)
        
        self.bot.handle_message = tracked_handle_message
        
        # Pornește bot-ul în fundal
        bot_task = asyncio.create_task(self.bot.start())
        
        try:
            # Așteaptă durata specificată
            await asyncio.sleep(duration)
            
        except KeyboardInterrupt:
            logger.info("\n⚠️  Test oprit de utilizator")
        
        finally:
            # Oprește bot-ul
            logger.info("🛑 Opresc bot-ul...")
            await self.bot.client.close()
            
            # Așteaptă task-ul să se termine
            try:
                await asyncio.wait_for(bot_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("⚠️  Timeout la oprirea bot-ului")
            except Exception as e:
                logger.debug(f"Task-ul bot-ului s-a terminat: {e}")
            
            # Afișează statistici
            self.print_statistics()
    
    def print_statistics(self):
        """Afișează statisticile testului"""
        print("\n" + "=" * 70)
        print("📊 STATISTICI TEST")
        print("=" * 70)
        print(f"\n✉️  Mesaje primite total: {self.messages_received}")
        print(f"🚀 Mesaje trimise către n8n: {self.messages_sent_to_n8n}")
        print(f"🤖 Mesaje ignorat (bot-uri): {self.messages_ignored}")
        
        if self.messages_received == 0:
            print("\n⚠️  ATENȚIE: Nu au fost primite mesaje!")
            print("   Verificări necesare:")
            print("   1. Bot-ul este adăugat pe server?")
            print("   2. Bot-ul are permisiuni să citească mesajele?")
            print("   3. Channel ID-ul este corect?")
            print("   4. Intent-urile sunt activate în Discord Developer Portal?")
        elif self.messages_sent_to_n8n > 0:
            print("\n✅ SUCCESS! Bot-ul:")
            print("   ✓ Primește mesaje de la Discord")
            print("   ✓ Procesează mesajele corect")
            print("   ✓ Trimite mesajele către n8n")
        else:
            print("\n⚠️  Bot-ul primește mesaje dar nu trimite către n8n")
            print("   Posibile cauze:")
            print("   - Toate mesajele sunt de la bot-uri")
            print("   - Mesajele sunt din canale nemonitorizate")
        
        print("\n" + "=" * 70)

async def main():
    """Funcția principală"""
    tester = BotLiveTester()
    
    # Rulează testul pentru 30 secunde (sau până la Ctrl+C)
    await tester.run_test(duration=30)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Test finalizat")
    except Exception as e:
        logger.error(f"💥 Eroare critică: {e}", exc_info=True)
        sys.exit(1)
