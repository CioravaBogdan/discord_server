import asyncio
import threading
import logging
from config import Config, setup_logging
from bot import DiscordBot
from webhook_server import run_webhook_server, set_bot_instance

# Setup logging
logger = setup_logging()

def run_webhook_in_thread():
    """Run the webhook server in a separate thread"""
    try:
        run_webhook_server()
    except Exception as e:
        logger.error(f"Eroare în serverul webhook: {e}")

async def main():
    """Main function that orchestrates the Discord bot and webhook server"""
    try:
        # Validate configuration
        Config.validate()
        logger.info("Configurația a fost validată cu succes")
        
        # Create Discord bot instance
        bot = DiscordBot()
        
        # Set bot instance for webhook server
        set_bot_instance(bot)
        
        # Start webhook server in a separate thread
        webhook_thread = threading.Thread(target=run_webhook_in_thread, daemon=True)
        webhook_thread.start()
        logger.info("Serverul webhook a fost pornit în thread separat")
        
        # Run the Discord bot (this will block)
        logger.info("Pornesc bot-ul Discord...")
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("Oprire prin Ctrl+C")
    except Exception as e:
        logger.error(f"Eroare în main: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program oprit de utilizator")
    except Exception as e:
        logger.error(f"Eroare critică: {e}")
        exit(1)
