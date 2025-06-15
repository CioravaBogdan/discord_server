import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MessageFilter:
    """Filtru pentru mesajele Discord pentru a preveni buclele"""
    
    def __init__(self):
        # Prefixuri care indică mesaje de la bot-uri
        self.bot_prefixes = ["🤖", "🚀", "⚡", "🔔", "📢"]
        
        # Nume de bot-uri cunoscute care ar trebui ignorate
        self.known_bots = [
            "infant_products",
            "INFANT.RO Bot", 
            "MEE6",
            "Carl-bot",
            "Dyno",
            "Mudae",
            "Rythm"
        ]
        
        # Pattern-uri de mesaje care ar trebui ignorate
        self.ignore_patterns = [
            r"^🤖.*",  # Mesaje care încep cu emoji de robot
            r".*\(automated\).*",  # Mesaje cu tag automated
            r".*powered by.*ai.*",  # Mesaje AI
            r".*infant\.ro.*powered by.*",  # Mesaje specifice site-ului
            r".*procesez.*fișiere.*",  # Mesaje de procesare
        ]
    
    def should_ignore_message(self, message_data: Dict[str, Any]) -> bool:
        """
        Determină dacă un mesaj ar trebui ignorat
        
        Args:
            message_data: Dicționar cu datele mesajului
            
        Returns:
            True dacă mesajul ar trebui ignorat, False altfel
        """
        
        # 1. Ignoră mesajele de la bot-uri
        if message_data.get('author', {}).get('is_bot', False):
            logger.debug("Mesaj ignorat: provine de la bot")
            return True
        
        # 2. Verifică numele autorului
        author_name = message_data.get('author', {}).get('username', '')
        if author_name.lower() in [bot.lower() for bot in self.known_bots]:
            logger.debug(f"Mesaj ignorat: autor cunoscut ca bot - {author_name}")
            return True
        
        # 3. Verifică prefixurile bot
        content = message_data.get('content', '')
        for prefix in self.bot_prefixes:
            if content.startswith(prefix):
                logger.debug(f"Mesaj ignorat: prefix bot detectat - {prefix}")
                return True
        
        # 4. Verifică pattern-urile
        for pattern in self.ignore_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                logger.debug(f"Mesaj ignorat: pattern detectat - {pattern}")
                return True
        
        # 5. Verifică dacă mesajul vine din n8n (are anumite caracteristici)
        if self._is_n8n_message(message_data):
            logger.debug("Mesaj ignorat: provine din n8n")
            return True
            
        return False
    
    def _is_n8n_message(self, message_data: Dict[str, Any]) -> bool:
        """Detectează mesajele care provin din n8n"""
        content = message_data.get('content', '').lower()
        
        # Indicatori că mesajul vine din n8n
        n8n_indicators = [
            'powered by ai',
            'infant.ro - powered by',
            'procesez',
            'analiza produs',
            'gemini ai',
            'analiza ai',
            'fișiere pentru analiza ai'
        ]
        
        return any(indicator in content for indicator in n8n_indicators)
    
    def add_bot_identifier(self, content: str) -> str:
        """Adaugă identificator că mesajul vine de la bot"""
        if not content.startswith("🤖"):
            return f"🤖 {content}"
        return content
    
    def get_stats(self) -> Dict[str, int]:
        """Returnează statistici despre filtrare"""
        return {
            'bot_prefixes_count': len(self.bot_prefixes),
            'known_bots_count': len(self.known_bots),
            'ignore_patterns_count': len(self.ignore_patterns)
        }
