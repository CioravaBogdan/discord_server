#!/usr/bin/env python3
"""
Test simplu pentru webhook-ul Discord bot
"""

import requests
import json

def test_webhook():
    """Test webhook endpoint"""
    webhook_url = "http://localhost:8000/send-message"
    
    # Data pentru test
    data = {
        "content": "🎉 Test mesaj din script - Discord bot este operațional în Docker!",
        "channel_id": 1383864616052068414
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Sending test message...")
        response = requests.post(webhook_url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Mesaj trimis cu succes!")
        else:
            print(f"❌ Eroare la trimiterea mesajului: {response.status_code}")
            
    except Exception as e:
        print(f"Eroare la conectare: {e}")

def test_health():
    """Test health endpoint"""
    health_url = "http://localhost:8000/health"
    
    try:
        print("Testing health endpoint...")
        response = requests.get(health_url)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.text}")
        
    except Exception as e:
        print(f"Eroare la health check: {e}")

if __name__ == "__main__":
    print("=== Test Discord Bot Webhook ===")
    test_health()
    print("\n" + "="*40 + "\n")
    test_webhook()