import os
import logging
from pathlib import Path
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
    
    # Webhook server settings - Docker compatible
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '0.0.0.0')
    WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8002'))  # New default port
    
    # Redis Configuration (for Docker)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Docker specific paths
    IS_DOCKER = os.getenv('DOCKER_ENV', 'false').lower() == 'true'
    LOG_DIR = Path('/app/logs') if IS_DOCKER else Path('./logs')
    DATA_DIR = Path('/app/data') if IS_DOCKER else Path('./data')
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Performance settings
    MAX_MESSAGE_CACHE = int(os.getenv('MAX_MESSAGE_CACHE', 1000))
    RATE_LIMIT_MESSAGES = int(os.getenv('RATE_LIMIT_MESSAGES', 30))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))
      # Health check settings
    HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', 30))
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_vars = ['BOT_TOKEN', 'N8N_WEBHOOK']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if cls.CHANNEL_ID == 0:
            missing_vars.append('CHANNEL_ID')
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Create directories if they don't exist
        cls.LOG_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Config validated - Docker mode: {cls.IS_DOCKER}")
        logger.info(f"Webhook server: {cls.WEBHOOK_HOST}:{cls.WEBHOOK_PORT}")

def setup_logging():
    """Setup logging configuration for both local and Docker environments"""
    log_file = Config.LOG_DIR / 'discord_bot.log'
    
    # Create handlers
    handlers = [
        logging.StreamHandler()  # Console output (important for Docker)
    ]
    
    # Add file handler if not in Docker or if explicitly requested
    if not Config.IS_DOCKER or os.getenv('LOG_TO_FILE', 'false').lower() == 'true':
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT,
        handlers=handlers
    )
    
    return logging.getLogger(__name__)
