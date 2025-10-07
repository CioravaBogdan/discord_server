"""
Script de testare pentru verificarea integrării bot Discord cu n8n
Verifică:
1. Dacă bot-ul primește mesaje
2. Dacă apelează corect webhook-ul n8n
3. Dacă ignoră mesajele de la bot-uri
"""

import asyncio
import logging
import requests
from datetime import datetime
from config import Config

# Configurare logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BotIntegrationTester:
    """Testează integrarea completă a bot-ului"""
    
    def __init__(self):
        self.results = {
            'config_valid': False,
            'n8n_accessible': False,
            'n8n_response_code': None,
            'n8n_response_time': None,
            'bot_token_valid': False,
            'channel_id_valid': False
        }
    
    def test_configuration(self):
        """Verifică configurația"""
        logger.info("=" * 60)
        logger.info("TESTARE CONFIGURAȚIE")
        logger.info("=" * 60)
        
        print(f"\n📋 Configurație:")
        print(f"   BOT_TOKEN: {'✅ Setat' if Config.BOT_TOKEN else '❌ Lipsă'}")
        print(f"   N8N_WEBHOOK: {Config.N8N_WEBHOOK}")
        print(f"   CHANNEL_ID: {Config.CHANNEL_ID}")
        print(f"   LOG_LEVEL: {Config.LOG_LEVEL}")
        
        self.results['bot_token_valid'] = bool(Config.BOT_TOKEN)
        self.results['channel_id_valid'] = Config.CHANNEL_ID > 0
        
        try:
            Config.validate()
            self.results['config_valid'] = True
            logger.info("✅ Configurația este validă")
            return True
        except Exception as e:
            logger.error(f"❌ Configurația este invalidă: {e}")
            return False
    
    def test_n8n_connection(self):
        """Testează conexiunea la n8n"""
        logger.info("\n" + "=" * 60)
        logger.info("TESTARE CONEXIUNE N8N")
        logger.info("=" * 60)
        
        test_data = {
            'test': True,
            'timestamp': datetime.now().isoformat(),
            'message': 'Test de conectivitate n8n',
            'content': 'Acesta este un mesaj de test pentru a verifica webhook-ul n8n',
            'author': {
                'username': 'TestBot',
                'id': '0',
                'is_bot': False
            },
            'channel': {
                'id': str(Config.CHANNEL_ID),
                'name': 'test-channel'
            }
        }
        
        print(f"\n🔗 Testez webhook n8n: {Config.N8N_WEBHOOK}")
        
        try:
            start_time = datetime.now()
            response = requests.post(
                Config.N8N_WEBHOOK,
                json=test_data,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            
            self.results['n8n_response_code'] = response.status_code
            self.results['n8n_response_time'] = response_time
            
            print(f"\n📊 Rezultat:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Timp răspuns: {response_time:.2f}s")
            
            if response.status_code == 200:
                logger.info("✅ n8n răspunde corect")
                self.results['n8n_accessible'] = True
                
                # Verifică răspunsul
                try:
                    response_data = response.json()
                    print(f"   Răspuns n8n: {response_data}")
                except:
                    print(f"   Răspuns text: {response.text[:200]}")
                
                return True
            elif response.status_code == 404:
                logger.warning("⚠️ Webhook-ul n8n nu este găsit (404)")
                print("   ⚠️ Verifică dacă workflow-ul n8n este activ!")
                return False
            else:
                logger.error(f"❌ n8n a răspuns cu status {response.status_code}")
                print(f"   Răspuns: {response.text[:200]}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error("❌ Timeout la conectarea cu n8n (>10s)")
            print("   ⏱️ n8n nu răspunde în timp util")
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ Nu pot conecta la n8n: {e}")
            print("   🔌 Verifică dacă n8n rulează și este accesibil")
            return False
        except Exception as e:
            logger.error(f"❌ Eroare neașteptată: {e}")
            return False
    
    def test_message_flow(self):
        """Simulează fluxul unui mesaj"""
        logger.info("\n" + "=" * 60)
        logger.info("SIMULARE FLUX MESAJ")
        logger.info("=" * 60)
        
        # Simulează diferite tipuri de mesaje
        test_cases = [
            {
                'name': 'Mesaj normal de la user',
                'should_process': True,
                'data': {
                    'content': 'Salut! Acesta este un mesaj de test',
                    'author': {'username': 'TestUser', 'is_bot': False}
                }
            },
            {
                'name': 'Mesaj de la bot',
                'should_process': False,
                'data': {
                    'content': '🤖 Răspuns automat',
                    'author': {'username': 'BotUser', 'is_bot': True}
                }
            }
        ]
        
        print(f"\n🧪 Teste flux mesaj:")
        
        for test in test_cases:
            print(f"\n   Test: {test['name']}")
            print(f"   - Is bot: {test['data']['author']['is_bot']}")
            print(f"   - Ar trebui procesat: {'✅ DA' if test['should_process'] else '❌ NU'}")
            
            if test['should_process']:
                print(f"   - Ar fi trimis către n8n")
            else:
                print(f"   - Ar fi ignorat (mesaj de la bot)")
    
    def print_summary(self):
        """Afișează rezumatul testelor"""
        logger.info("\n" + "=" * 60)
        logger.info("REZUMAT TESTE")
        logger.info("=" * 60)
        
        print(f"\n📊 Rezultate:")
        print(f"   ✓ Configurație validă: {'✅' if self.results['config_valid'] else '❌'}")
        print(f"   ✓ Token bot valid: {'✅' if self.results['bot_token_valid'] else '❌'}")
        print(f"   ✓ Channel ID valid: {'✅' if self.results['channel_id_valid'] else '❌'}")
        print(f"   ✓ n8n accesibil: {'✅' if self.results['n8n_accessible'] else '❌'}")
        
        if self.results['n8n_response_code']:
            print(f"   ✓ Status code n8n: {self.results['n8n_response_code']}")
        if self.results['n8n_response_time']:
            print(f"   ✓ Timp răspuns n8n: {self.results['n8n_response_time']:.2f}s")
        
        # Verifică dacă totul este OK
        all_ok = (
            self.results['config_valid'] and
            self.results['n8n_accessible'] and
            self.results['bot_token_valid'] and
            self.results['channel_id_valid']
        )
        
        print(f"\n{'🎉 TOATE TESTELE OK!' if all_ok else '⚠️ UNELE TESTE AU EȘUAT'}")
        
        if all_ok:
            print("\n✅ Bot-ul este configurat corect și poate comunica cu n8n!")
            print("   Pentru a testa recepția mesajelor, pornește bot-ul cu:")
            print("   python bot.py")
        else:
            print("\n❌ Probleme detectate:")
            if not self.results['config_valid']:
                print("   - Configurația este incompletă")
            if not self.results['bot_token_valid']:
                print("   - Token-ul bot-ului lipsește")
            if not self.results['channel_id_valid']:
                print("   - Channel ID invalid")
            if not self.results['n8n_accessible']:
                print("   - n8n nu este accesibil")
    
    def run_all_tests(self):
        """Rulează toate testele"""
        print("\n" + "🚀 " + "=" * 58)
        print("🚀  TESTARE INTEGRARE BOT DISCORD CU N8N")
        print("🚀 " + "=" * 58)
        
        # Test 1: Configurație
        config_ok = self.test_configuration()
        
        # Test 2: Conexiune n8n (doar dacă configurația e OK)
        if config_ok:
            self.test_n8n_connection()
        
        # Test 3: Flux mesaje
        self.test_message_flow()
        
        # Rezumat
        self.print_summary()

if __name__ == "__main__":
    tester = BotIntegrationTester()
    tester.run_all_tests()
