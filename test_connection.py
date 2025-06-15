import requests
import json
from config import Config

def test_n8n_connection():
    """Test connection to n8n webhook"""
    try:
        # Test data
        test_data = {
            "content": "Test connection from Discord bot",
            "timestamp": "2025-06-15T10:30:00.000Z",
            "message_id": "test_123",
            "channel": {
                "id": "123456789",
                "name": "test-channel"
            },
            "author": {
                "id": "987654321",
                "username": "test_user",
                "display_name": "Test User"
            },
            "attachments": []
        }
        
        print(f"Testing connection to: {Config.N8N_WEBHOOK}")
        
        response = requests.post(
            Config.N8N_WEBHOOK,
            json=test_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Connection to n8n successful!")
        else:
            print(f"❌ Connection failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to n8n. Make sure n8n is running and the URL is correct.")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_discord_webhook():
    """Test Discord webhook server"""
    try:
        print(f"Testing Discord webhook server at: http://localhost:{Config.WEBHOOK_PORT}")
        
        response = requests.get(f"http://localhost:{Config.WEBHOOK_PORT}/health")
        
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Discord webhook server is running!")
        else:
            print(f"❌ Webhook server issue: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Discord webhook server is not running. Start it with 'python main.py'")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔧 Testing Discord Bot <-> n8n Integration")
    print("=" * 50)
    
    # Load config
    try:
        Config.validate()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        exit(1)
    
    print("\n1. Testing n8n connection...")
    test_n8n_connection()
    
    print("\n2. Testing Discord webhook server...")
    test_discord_webhook()
    
    print("\n🎯 Next steps:")
    print("1. Make sure n8n has a webhook at the configured URL")
    print("2. Create workflows in n8n to process Discord messages")
    print("3. Update CHANNEL_ID in .env with your actual Discord channel ID")
    print("4. Start the bot with: python main.py")
