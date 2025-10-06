import os
from dotenv import load_dotenv

load_dotenv()

print("=== VERIFICARE CONFIGURAȚIE ===")
bot_token = os.getenv('BOT_TOKEN', 'NU SETAT')
print(f"BOT_TOKEN: {bot_token[:20] if bot_token != 'NU SETAT' else bot_token}...")
print(f"CHANNEL_ID: {os.getenv('CHANNEL_ID', 'NU SETAT')}")
print(f"N8N_WEBHOOK: {os.getenv('N8N_WEBHOOK', 'NU SETAT')}")
print("==============================")

# Test import
try:
    from config import Config
    Config.validate()
    print("✅ Configurația este validă!")
except Exception as e:
    print(f"❌ Eroare configurație: {e}")
