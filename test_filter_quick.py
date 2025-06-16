#!/usr/bin/env python3
"""
Test rapid pentru filtrele de mesaje - să vedem dacă blochează mesajele normale
"""
from message_filters import MessageFilter

def test_normal_messages():
    """Test cu mesaje normale care NU ar trebui să fie blocate"""
    filter = MessageFilter()
    
    test_messages = [
        {
            'content': 'Salut, cum merge?',
            'author': {'username': 'user1', 'display_name': 'User1', 'is_bot': False}
        },
        {
            'content': 'Ce faci azi?',
            'author': {'username': 'user2', 'display_name': 'User2', 'is_bot': False}
        },
        {
            'content': 'Am comandat de la infant.ro',
            'author': {'username': 'user3', 'display_name': 'User3', 'is_bot': False}
        },
        {
            'content': 'Mulțumesc pentru ajutor!',
            'author': {'username': 'user4', 'display_name': 'User4', 'is_bot': False}
        },
        {
            'content': 'Aveți stoc la acest produs?',
            'author': {'username': 'user5', 'display_name': 'User5', 'is_bot': False}
        }
    ]
    
    print("🧪 Testez mesaje normale (nu ar trebui să fie blocate):")
    for i, message in enumerate(test_messages, 1):
        should_ignore = filter.should_ignore_message(message)
        status = "❌ BLOCAT" if should_ignore else "✅ TRECUT"
        print(f"{i}. {status} - '{message['content']}'")
        
        if should_ignore:
            print(f"   ⚠️  PROBLEMĂ: Mesajul normal a fost blocat!")
    
    print("\n🧪 Testez mesaje cu bot-uri (ar trebui să fie blocate):")
    bot_messages = [
        {
            'content': '🤖 Mesaj automat de la bot',
            'author': {'username': 'bot1', 'display_name': 'Bot1', 'is_bot': False}
        },
        {
            'content': 'Mesaj normal',
            'author': {'username': 'real_bot', 'display_name': 'RealBot', 'is_bot': True}
        },
        {
            'content': '🤖🔒 Mesaj de la n8n',
            'author': {'username': 'user6', 'display_name': 'User6', 'is_bot': False}
        }
    ]
    
    for i, message in enumerate(bot_messages, 1):
        should_ignore = filter.should_ignore_message(message)
        status = "✅ BLOCAT" if should_ignore else "❌ TRECUT"
        print(f"{i}. {status} - '{message['content']}'")

if __name__ == "__main__":
    test_normal_messages()
