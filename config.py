import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Discord bot and n8n integration"""
    
    # Discord bot settings
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = int(os.getenv('CHANNEL_ID', '0'))
    
    # n8n webhook settings
    N8N_WEBHOOK = os.getenv('N8N_WEBHOOK')
    
    # Webhook server settings
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8000'))
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        if not cls.N8N_WEBHOOK:
            raise ValueError("N8N_WEBHOOK environment variable is required")
        if cls.CHANNEL_ID == 0:
            raise ValueError("CHANNEL_ID environment variable is required")

def setup_logging():
    """Setup logging configuration"""
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    return logger
