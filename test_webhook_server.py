#!/usr/bin/env python3
"""
Test webhook server - verifică că serverul local poate primi cereri
"""

import requests
import asyncio
import threading
import time
import sys
from webhook_server import run_webhook_server
from config import Config

def start_webhook_server():
    """Pornește webhook server-ul într-un thread separat"""
    try:
        run_webhook_server()
    except Exception as e:
        print(f"Eroare server webhook: {e}")

def test_webhook_server():
    """Testează webhook server-ul local"""
    print("🌐 TESTEZ WEBHOOK SERVER LOCAL...")
    
    # Pornește server-ul într-un thread
    server_thread = threading.Thread(target=start_webhook_server, daemon=True)
    server_thread.start()
    
    print("⏳ Aștept să pornească server-ul...")
    time.sleep(3)  # Așteaptă să pornească
    
    try:
        # Test health check
        health_url = f"http://localhost:{Config.WEBHOOK_PORT}/health"
        print(f"🔍 Testez health check: {health_url}")
        
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Nu pot conecta la webhook server")
        return False
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 TEST WEBHOOK SERVER LOCAL")
    print("=" * 50)
    
    try:
        result = test_webhook_server()
        if result:
            print("\n🎉 WEBHOOK SERVER FUNCȚIONEAZĂ!")
        else:
            print("\n❌ Webhook server nu funcționează")
            
        print("\n⏰ Opresc testul în 2 secunde...")
        time.sleep(2)
        
    except KeyboardInterrupt:
        print("\n✅ Test oprit manual")
    except Exception as e:
        print(f"\n❌ Eroare: {e}")
        sys.exit(1)
