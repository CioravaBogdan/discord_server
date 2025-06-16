#!/usr/bin/env python3
"""
Test pentru verificarea detectării header-ului X-Source: n8n-automation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from message_filters import MessageFilter

def test_n8n_header_detection():
    """Test enhanced filtering with n8n header detection"""
    filter = MessageFilter()
    
    test_cases = [
        # Should be ignored (n8n automation messages)
        {
            'name': 'N8N message with anti-loop prefix',
            'data': {
                'content': '🤖🔒 🚀 **INFANT.RO Bot a pornit procesarea!**',
                'author': {'username': 'infant_products', 'display_name': 'INFANT.RO Bot', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'N8N automated processing message',
            'data': {
                'content': '🤖🔒 📦 Analiză Produs Nouă - Am primit fișiere pentru analiza AI',
                'author': {'username': 'user123', 'display_name': 'User', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Original n8n pattern without prefix',
            'data': {
                'content': '🚀 **INFANT.RO Bot a pornit procesarea!**',
                'author': {'username': 'infant_products', 'display_name': 'INFANT.RO Bot', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'N8N powered by AI message',
            'data': {
                'content': 'INFANT.RO - Powered by AI - Cod Produs: ABC123',
                'author': {'username': 'user123', 'display_name': 'User', 'is_bot': False}
            },
            'should_ignore': True
        },
        
        # Should be processed (legitimate user messages)
        {
            'name': 'Normal user message',
            'data': {
                'content': 'Hello, I have a question about this product',
                'author': {'username': 'customer123', 'display_name': 'Customer', 'is_bot': False}
            },
            'should_ignore': False
        },
        {
            'name': 'User question in Romanian',
            'data': {
                'content': 'Salut, am o întrebare despre acest produs. Cât costă?',
                'author': {'username': 'utilizator456', 'display_name': 'Utilizator', 'is_bot': False}
            },
            'should_ignore': False
        },
        {
            'name': 'User sharing file',
            'data': {
                'content': 'Am atașat imaginea cu produsul',
                'author': {'username': 'user789', 'display_name': 'User', 'is_bot': False}
            },
            'should_ignore': False
        }
    ]
    
    print("🧪 N8N Header Detection Test")
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
        print(f"   Content: {test['data']['content'][:60]}...")
        print(f"   Author: {test['data']['author']['username']}")
        print(f"   Expected: {'Ignore' if expected else 'Process'}")
        print(f"   Got: {'Ignore' if result else 'Process'}")
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed! N8N header detection is working correctly.")
        print("✅ Messages with 🤖🔒 prefix will be ignored")
        print("✅ N8N automation patterns are detected")
        print("✅ User messages will be processed normally")
    else:
        print("❌ Some tests failed! Please check the filtering logic.")
    
    return passed == total

def test_prefix_functionality():
    """Test the add_bot_identifier function"""
    filter = MessageFilter()
    
    test_cases = [
        {
            'input': 'Normal message',
            'expected': '🤖 Normal message'
        },
        {
            'input': '🤖 Already has prefix',
            'expected': '🤖 Already has prefix'
        },
        {
            'input': '🤖🔒 Anti-loop prefix',
            'expected': '🤖🔒 Anti-loop prefix'
        },
        {
            'input': '🚀 Different emoji prefix',
            'expected': '🚀 Different emoji prefix'
        }
    ]
    
    print("🔧 Bot Identifier Test")
    print("=" * 40)
    
    passed = 0
    total = len(test_cases)
    
    for test in test_cases:
        result = filter.add_bot_identifier(test['input'])
        expected = test['expected']
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        
        print(f"{status} Input: '{test['input']}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got: '{result}'")
        print()
    
    print(f"📊 Results: {passed}/{total} tests passed")
    return passed == total

if __name__ == "__main__":
    print("🚀 Testing N8N Integration Anti-Loop System")
    print("=" * 80)
    print()
    
    test1_success = test_n8n_header_detection()
    print()
    test2_success = test_prefix_functionality()
    
    print("\n" + "=" * 80)
    if test1_success and test2_success:
        print("🎉 ALL TESTS PASSED! Anti-loop system is ready!")
        exit(0)
    else:
        print("❌ SOME TESTS FAILED! Please fix the issues.")
        exit(1)
