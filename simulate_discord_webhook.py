#!/usr/bin/env python3
"""
Simulează exact ce ar trimite bot-ul către n8n
"""
import requests
import json
from datetime import datetime
from config import Config

def simulate_discord_message():
    """Simulează un mesaj Discord trimis către n8n"""
    
    # Simulez exact datele pe care le-ar trimite bot-ul
    message_data = {
        'content': 'Test manual din script - simulez mesaj Discord',
        'message_id': '1234567890123456789',
        'timestamp': datetime.now().isoformat(),
        'channel': {
            'id': Config.CHANNEL_ID,
            'name': 'general'
        },
        'author': {
            'id': '987654321098765432',
            'username': 'test_user',
            'display_name': 'Test User',
            'is_bot': False
        },
        'guild': {
            'id': '1383864609379319878',
            'name': 'Test Server'
        },
        'attachments': []
    }
    
    print(f"🚀 Trimit simulare mesaj Discord către n8n...")
    print(f"📤 URL: {Config.N8N_WEBHOOK}")
    print(f"📝 Content: {message_data['content']}")
    
    try:
        response = requests.post(
            Config.N8N_WEBHOOK,
            json=message_data,
            timeout=10,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'DiscordBot/1.0'
            }
        )
        
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.text}")
        
        if response.status_code == 200:
            print("🎉 Simularea a reușit! N8N primește datele corect.")
            return True
        else:
            print("❌ Problemă cu răspunsul n8n!")
            return False
            
    except Exception as e:
        print(f"❌ Eroare: {str(e)}")
        return False

if __name__ == "__main__":
    simulate_discord_message()
