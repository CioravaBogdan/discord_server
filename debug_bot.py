#!/usr/bin/env python3
"""
Script pentru a porni bot-ul Discord cu logging îmbunătățit pentru debugging
"""
import asyncio
import logging
import sys
from pathlib import Path

# Adăugare path pentru a putea importa modulele
sys.path.append(str(Path(__file__).parent))

from config import Config
from bot import DiscordBot

# Setup logging cu mai multe detalii
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_debug.log')
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Pornește bot-ul cu debugging îmbunătățit"""
    try:
        logger.info("🚀 Pornesc bot-ul Discord cu debugging complet...")
        
        # Validare configurație
        Config.validate()
        logger.info(f"✅ Configurație validată - Canal: {Config.CHANNEL_ID}")
        logger.info(f"✅ N8N Webhook: {Config.N8N_WEBHOOK}")
        
        # Creare instanță bot
        bot = DiscordBot()
        logger.info("✅ Bot creat cu succes")
        
        # Pornire bot
        await bot.start()
        
    except Exception as e:
        logger.error(f"💥 Eroare critică: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot oprit de utilizator")
    except Exception as e:
        logger.error(f"💥 Eroare în main: {str(e)}")
