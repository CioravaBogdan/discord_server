from message_filters import MessageFilter

def test_message_filtering():
    """Test pentru verificarea filtrării mesajelor"""
    filter = MessageFilter()
    
    # Test cases
    test_messages = [
        {
            'name': 'Mesaj normal utilizator',
            'data': {
                'content': 'Salut, cum merge?',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': False
        },
        {
            'name': 'Mesaj de la bot Discord',
            'data': {
                'content': 'Mesaj automat',
                'author': {'username': 'infant_products', 'is_bot': True}
            },
            'should_ignore': True
        },        {
            'name': 'Mesaj cu prefix bot',
            'data': {
                'content': '🤖 Răspuns automat din n8n',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Mesaj cu prefix anti-buclă n8n',
            'data': {
                'content': '🤖🔒 Răspuns automat din n8n pentru a preveni bucla',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Mesaj n8n detectat prin conținut',
            'data': {
                'content': 'INFANT.RO - Powered by Gemini AI',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Mesaj de analiză produs',
            'data': {
                'content': 'Procesez 3 fișiere pentru analiza AI',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': True
        },
        {
            'name': 'Mesaj bot cunoscut (MEE6)',
            'data': {
                'content': 'Level up!',
                'author': {'username': 'MEE6', 'is_bot': True}
            },
            'should_ignore': True
        },
        {
            'name': 'Mesaj normal cu emoji',
            'data': {
                'content': '😊 Bună ziua tuturor!',
                'author': {'username': 'user456', 'is_bot': False}
            },
            'should_ignore': False
        }
    ]
    
    print("🧪 Test Filtrare Mesaje Discord")
    print("=" * 60)
    
    total_tests = len(test_messages)
    passed_tests = 0
    
    for i, test in enumerate(test_messages, 1):
        result = filter.should_ignore_message(test['data'])
        status = "✅ PASS" if result == test['should_ignore'] else "❌ FAIL"
        
        if result == test['should_ignore']:
            passed_tests += 1
        
        print(f"Test {i}/{total_tests}: {status}")
        print(f"   📝 {test['name']}")
        print(f"   💬 Content: {test['data']['content'][:40]}...")
        print(f"   👤 Author: {test['data']['author']['username']} (bot: {test['data']['author']['is_bot']})")
        print(f"   📊 Expected: {'Ignore' if test['should_ignore'] else 'Process'}")
        print(f"   📊 Got: {'Ignore' if result else 'Process'}")
        print()
    print("=" * 60)
    print(f"📈 Rezultate: {passed_tests}/{total_tests} teste trecute")
    
    # Afișează statistici filtru
    stats = filter.get_stats()
    print(f"📊 Statistici filtru:")
    print(f"   • Prefixuri bot: {stats['bot_prefixes_count']}")
    print(f"   • Bot-uri cunoscute: {stats['known_bots_count']}")
    print(f"   • Pattern-uri bot: {stats['bot_patterns_count']}")
    print(f"   • Indicatori n8n: {stats['n8n_indicators_count']}")
    
    if passed_tests == total_tests:
        print("\n🎉 Toate testele au trecut! Filtrarea funcționează corect.")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} teste au eșuat. Verifică configurația.")
    
    # Use pytest assertion
    assert passed_tests == total_tests, f"Only {passed_tests}/{total_tests} tests passed"

if __name__ == "__main__":
    test_message_filtering()
