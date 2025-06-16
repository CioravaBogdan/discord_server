import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MessageFilter:
    """Enhanced message filter to prevent loops and duplicates"""
    
    def __init__(self):        # Bot prefixes that indicate automated messages
        self.bot_prefixes = [
            "🤖🔒",  # Special anti-loop prefix for n8n messages
            "🤖", "🚀", "⚡", "🔔", "📢", "🔥", "✨", "⭐", "💡",
            "📊", "📈", "📋", "🎯", "🛠️", "⚙️", "🔧", "📦"
        ]
        
        # Known bot names that should be ignored
        self.known_bots = [
            "infant_products",
            "infant.ro bot", 
            "mee6",
            "carl-bot",
            "dyno",
            "rythm",
            "groovy",
            "dank memer",
            "ticket tool",
            "statbot"
        ]
          # Patterns that indicate automated/bot messages
        self.bot_patterns = [
            r"^🤖🔒.*",  # Special anti-loop pattern for n8n
            r"^🤖.*",
            r".*\(automated\).*",
            r".*powered by.*ai.*",
            r".*infant\.ro.*powered by.*",
            r".*gemini ai.*",
            r".*procesez.*fișier.*",
            r".*analiză.*produs.*",
            r".*cod produs.*",
            r".*trimis de.*",
            r".*status.*în procesare.*",
            r".*video-uri.*imagini.*",
            r"🔥.*a pornit procesarea.*",
            r".*infant\.ro bot.*pornit.*"
        ]
        
        # Message content that indicates n8n generated content
        self.n8n_indicators = [
            "infant.ro - powered by",
            "procesez",
            "analiza produs", 
            "gemini ai",
            "cod produs",
            "trimis de",
            "imagini",
            "video-uri",
            "în procesare",
            "a pornit procesarea"
        ]

    def should_ignore_message(self, message_data: Dict[str, Any]) -> bool:
        """
        Enhanced filtering to prevent message loops
        """
        content = message_data.get('content', '').lower().strip()
        author = message_data.get('author', {})
        author_name = author.get('username', '').lower()
        display_name = author.get('display_name', '').lower()
        is_bot = author.get('is_bot', False)
        
        # 1. ALWAYS ignore if author is marked as bot
        if is_bot:
            logger.debug(f"Ignored: Bot author detected - {author_name}")
            return True
        
        # 2. Check known bot names (case insensitive)
        for bot_name in self.known_bots:
            if bot_name in author_name or bot_name in display_name:
                logger.debug(f"Ignored: Known bot name - {author_name}")
                return True
        
        # 3. Check bot prefixes
        for prefix in self.bot_prefixes:
            if content.startswith(prefix.lower()):
                logger.debug(f"Ignored: Bot prefix detected - {prefix}")
                return True
        
        # 4. Check automated message patterns
        for pattern in self.bot_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                logger.debug(f"Ignored: Bot pattern matched - {pattern}")
                return True
        
        # 5. Check n8n specific indicators
        for indicator in self.n8n_indicators:
            if indicator.lower() in content:
                logger.debug(f"Ignored: n8n indicator found - {indicator}")
                return True
        
        # 6. Check if message looks like a repeated/duplicate message
        if self._is_duplicate_pattern(content):
            logger.debug(f"Ignored: Duplicate pattern detected")
            return True
          # 7. Check webhook/system message characteristics
        if self._is_system_message(message_data):
            logger.debug(f"Ignored: System message detected")
            return True
            
        return False
    
    def _is_duplicate_pattern(self, content: str) -> bool:
        """Check if message looks like a duplicate/repeated message"""
        duplicate_patterns = [
            r"(\b\w{3,}\b)\s+\1",  # Repeated words (3+ chars)
            r"^(.{10,})\s+\1",  # Repeated longer phrases (10+ chars)
            r"^(.{1,5})\1{4,}",  # Repeated short sequences (4+ times)
        ]
        
        for pattern in duplicate_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _is_system_message(self, message_data: Dict[str, Any]) -> bool:
        """Check if message has system/webhook characteristics"""
        
        # Check message structure for webhook indicators
        content = message_data.get('content', '')
        
        # Messages with structured data (likely from webhooks)
        structured_indicators = [
            'timestamp',
            'message_id', 
            'channel_id',
            'user_id',
            '{"',
            'http://',
            'https://',
            'webhook'
        ]
        
        content_lower = content.lower()
        webhook_indicator_count = sum(1 for indicator in structured_indicators if indicator in content_lower)
        
        # If multiple webhook indicators, likely a system message
        if webhook_indicator_count >= 2:
            return True
            
        return False

    def add_bot_identifier(self, content: str) -> str:
        """Add bot identifier to outgoing messages"""
        if not any(content.startswith(prefix) for prefix in self.bot_prefixes):
            return f"🤖 {content}"
        return content

    def get_stats(self) -> Dict[str, int]:
        """Get filtering statistics"""
        return {
            'bot_prefixes_count': len(self.bot_prefixes),
            'known_bots_count': len(self.known_bots),
            'bot_patterns_count': len(self.bot_patterns),
            'n8n_indicators_count': len(self.n8n_indicators)
        }
