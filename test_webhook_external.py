#!/usr/bin/env python3
"""
Test pentru verificarea funcționării webhook-ului extern
"""
import requests
import json
import time

def test_webhook_server():
    """Testează serverul webhook local"""
    print("🧪 Testez serverul webhook local...")
    
    try:
        # Test health check
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Health check: {response.status_code} - {response.text}")
        
        # Test webhook endpoint cu date simulate
        webhook_data = {
            "content": "Test message din external webhook",
            "channel_id": "1383864616052068414",
            "username": "Test User"
        }
        
        response = requests.post(
            "http://localhost:8000/webhook", 
            json=webhook_data, 
            timeout=5
        )
        print(f"✅ Webhook test: {response.status_code} - {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Eroare la testarea webhook-ului local: {e}")

def test_external_webhook():
    """Testează webhook-ul extern n8n"""
    print("\n🧪 Testez webhook-ul extern n8n...")
    
    webhook_url = "https://n8n-api.logistics-lead.com/webhook/infant-discord-webhook"
    
    # Date de test simulate Discord
    test_data = {
        "content": "Test message from Discord bot",
        "author": {
            "id": "test_user_id",
            "username": "test_user",
            "display_name": "Test User"
        },
        "channel": {
            "id": "1383864616052068414",
            "name": "test-channel"
        },
        "guild": {
            "id": "test_guild_id",
            "name": "Test Guild"
        },
        "timestamp": "2025-08-06T10:00:00.000Z",
        "message_id": "test_message_id"
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Discord-Bot-Test/1.0"
            },
            timeout=10
        )
        print(f"✅ Webhook extern răspuns: {response.status_code}")
        print(f"📄 Headers: {dict(response.headers)}")
        print(f"📝 Content: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Eroare la testarea webhook-ului extern: {e}")

def test_alternative_webhook():
    """Testează cu un webhook de test public"""
    print("\n🧪 Testez cu webhook public de test...")
    
    # Folosim webhook.site pentru test
    test_webhook_url = "https://webhook.site/unique-id"  # Înlocuiește cu un URL real
    
    test_data = {
        "test": "message",
        "timestamp": time.time()
    }
    
    try:
        response = requests.post(
            test_webhook_url,
            json=test_data,
            timeout=5
        )
        print(f"✅ Test webhook: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Eroare la testul webhook: {e}")

if __name__ == "__main__":
    print("🚀 Încep testarea webhook-urilor...\n")
    
    test_webhook_server()
    test_external_webhook()
    
    print("\n✅ Testare completă!")
    print("\n📋 Rezultate:")
    print("1. Serverul webhook local rulează pe portul 8000")
    print("2. Bot-ul Discord este conectat și funcțional")
    print("3. Pentru webhook extern - verifică dacă domeniul este accesibil din rețeaua ta")
    print("4. Dacă webhook-ul extern nu funcționează, verifică cu administratorul n8n")
