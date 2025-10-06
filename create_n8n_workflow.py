#!/usr/bin/env python3
"""
Script pentru a crea automat workflow-ul Discord în n8n
"""
import requests
import json
import time

N8N_URL = "http://localhost:5678"

def create_discord_workflow():
    """Creează workflow-ul Discord în n8n"""
    
    # Workflow definition
    workflow = {
        "name": "Discord Bot Integration",
        "nodes": [
            {
                "id": "webhook-node",
                "name": "Discord Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "discord-bot",
                    "responseMode": "onReceived",
                    "responseData": "firstEntryJson"
                }
            },
            {
                "id": "code-node", 
                "name": "Process Discord Data",
                "type": "n8n-nodes-base.code",
                "typeVersion": 1,
                "position": [450, 300],
                "parameters": {
                    "language": "javascript",
                    "jsCode": """
// Procesează datele primite de la Discord
const discordData = $input.all()[0].json;

console.log('📨 Mesaj Discord primit:', discordData.content);
console.log('👤 De la:', discordData.author?.username || 'Unknown');

// Verifică cuvinte cheie pentru atenție specială
const keywords = ['help', 'urgent', 'problem', 'bug', 'error', 'issue'];
const needsAttention = keywords.some(keyword => 
  discordData.content?.toLowerCase().includes(keyword)
);

// Verifică atașamente
const hasFiles = discordData.attachments && discordData.attachments.length > 0;

// Pregătește răspunsul
const response = {
  originalMessage: discordData,
  processed: true,
  needsAttention: needsAttention,
  hasFiles: hasFiles,
  processedAt: new Date().toISOString(),
  summary: `${discordData.author?.username || 'User'}: ${(discordData.content || '').substring(0, 100)}...`,
  keywords_found: keywords.filter(k => discordData.content?.toLowerCase().includes(k))
};

console.log('✅ Mesaj procesat:', response.summary);

return [{ json: response }];
"""
                }
            }
        ],
        "connections": {
            "Discord Webhook": {
                "main": [
                    [
                        {
                            "node": "Process Discord Data",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True,
        "settings": {
            "saveManualExecutions": True
        },
        "tags": ["discord", "bot", "webhook"]
    }
    
    try:
        # Creează workflow-ul
        response = requests.post(
            f"{N8N_URL}/api/v1/workflows",
            json=workflow,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            workflow_data = response.json()
            print(f"✅ Workflow creat cu succes!")
            print(f"📋 ID Workflow: {workflow_data.get('id')}")
            print(f"🔗 Webhook URL: {N8N_URL}/webhook/discord-bot")
            return workflow_data
        else:
            print(f"❌ Eroare la crearea workflow-ului: {response.status_code}")
            print(f"📝 Răspuns: {response.text}")
            return None
            
    except Exception as e:
        print(f"💥 Excepție: {str(e)}")
        return None

def test_webhook():
    """Testează webhook-ul creat"""
    test_data = {
        "content": "Test message from script",
        "author": {
            "username": "test_user"
        },
        "attachments": [],
        "timestamp": "2025-06-19T12:00:00.000Z"
    }
    
    try:
        response = requests.post(
            f"{N8N_URL}/webhook/discord-bot",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Webhook funcționează corect!")
            print(f"📝 Răspuns: {response.text}")
            return True
        else:
            print(f"❌ Webhook nu funcționează: {response.status_code}")
            print(f"📝 Răspuns: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Eroare la testare: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Creez workflow-ul Discord în n8n...")
    
    # Verifică dacă n8n este accesibil
    try:
        health_check = requests.get(f"{N8N_URL}/api/v1/workflows")
        if health_check.status_code != 200:
            print(f"❌ n8n nu este accesibil: {health_check.status_code}")
            exit(1)
    except Exception as e:
        print(f"❌ Nu pot accesa n8n: {str(e)}")
        exit(1)
    
    # Creează workflow-ul
    workflow = create_discord_workflow()
    
    if workflow:
        print("\n⏳ Aștept 3 secunde pentru activarea workflow-ului...")
        time.sleep(3)
        
        # Testează webhook-ul
        print("\n🧪 Testez webhook-ul...")
        test_webhook()
    
    print("\n🎉 Configurare completă!")
