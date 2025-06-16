#!/usr/bin/env python3
"""
Test script for enhanced message filtering
"""

from message_filters import MessageFilter

def test_enhanced_filtering():
    """Test enhanced message filtering"""
    filter = MessageFilter()
    
    test_cases = [
        # Should be processed (legitimate user messages)
        {
            'name': 'Normal user message',
            'data': {
                'content': 'Hello, how are you?',
                'author': {'username': 'john_doe', 'display_name': 'John', 'is_bot': False}
            },
            'should_ignore': False
        },
        {
            'name': 'User question',
            'data': {
                'content': 'Care este prețul pentru acest produs?',
                'author': {'username': 'customer123', 'display_name': 'Customer', 'is_bot': False}
            },
            'should_ignore': False
        },
        
        # Should be ignored (bot messages)
        {
            'name': 'Bot flag set',
            'data': {
                'content': 'Any message from actual bot',
                'author': {'username': 'some_bot', 'display_name': 'Bot', 'is_bot': True}
            },
            'should_ignore': True
        },
        {
            'name': 'INFANT.RO Bot message',
            'data': {
                'content': 'INFANT.RO Bot a pornit procesarea!',
                'author': {'username': 'infant_products', 'display_name': 'INFANT.RO Bot', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Message with bot prefix',
            'data': {
                'content': '🤖 Automated response from n8n',
                'author': {'username': 'user123', 'display_name': 'User', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'n8n powered message',
            'data': {
                'content': 'INFANT.RO - Powered by Gemini AI Today at 9:52 AM',
                'author': {'username': 'user123', 'display_name': 'User', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Processing message',
            'data': {
                'content': 'Procesez fișier pentru analiza AI',
                'author': {'username': 'user123', 'display_name': 'User', 'is_bot': False}
            },
            'should_ignore': True
        }
    ]
    
    print("🧪 Enhanced Message Filtering Test")
    print("=" * 60)
    
    passed = 0
    total = len(test_cases)
    
    for test in test_cases:
        result = filter.should_ignore_message(test['data'])
        expected = test['should_ignore']
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        
        print(f"{status} {test['name']}")
        print(f"   Content: {test['data']['content'][:40]}...")
        print(f"   Author: {test['data']['author']['username']}")
        print(f"   Expected: {'Ignore' if expected else 'Process'}")
        print(f"   Got: {'Ignore' if result else 'Process'}")
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    return passed == total

if __name__ == "__main__":
    success = test_enhanced_filtering()
    exit(0 if success else 1)
