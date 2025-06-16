#!/usr/bin/env python3
import requests
import json
from config import Config

def test_n8n_webhook():
    """Test rapid pentru webhook-ul n8n"""
    print(f"🧪 Testez webhook-ul n8n: {Config.N8N_WEBHOOK}")
    
    test_data = {
        "test": True,
        "message": "Test manual de la Discord bot",
        "timestamp": "2025-06-16T12:00:00Z"
    }
    
    try:
        response = requests.post(
            Config.N8N_WEBHOOK,
            json=test_data,
            timeout=10,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'DiscordBot/1.0-TEST'
            }
        )
        
        print(f"✅ Status: {response.status_code}")
        print(f"📝 Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("🎉 Webhook-ul n8n funcționează!")
            return True
        else:
            print("❌ Webhook-ul n8n nu răspunde corect!")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Nu mă pot conecta la n8n webhook!")
        return False
    except Exception as e:
        print(f"❌ Eroare: {str(e)}")
        return False

if __name__ == "__main__":
    test_n8n_webhook()
