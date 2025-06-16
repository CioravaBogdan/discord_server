#!/usr/bin/env python3
"""
Test specific pentru funcționalitatea anti-buclă
Testează prevenirea re-procesării mesajelor cu prefix 🤖🔒
"""

import sys
import requests
import json
from message_filters import MessageFilter

def test_anti_loop_prefix():
    """Test specific pentru prefix-ul anti-buclă 🤖🔒"""
    filter = MessageFilter()
    
    # Test cases specific pentru anti-loop
    test_cases = [
        {
            'name': 'Mesaj normal fără prefix',
            'data': {
                'content': 'Acesta este un mesaj normal de la utilizator',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': False,
            'description': 'Mesajele normale trebuie procesate'
        },
        {
            'name': 'Mesaj cu prefix anti-buclă',
            'data': {
                'content': '🤖🔒 Acest mesaj vine de la n8n și nu trebuie re-procesat',
                'author': {'username': 'user123', 'is_bot': False}
            },
            'should_ignore': True,
            'description': 'Mesajele cu 🤖🔒 trebuie ignorate'
        },
        {
            'name': 'Mesaj cu prefix anti-buclă și conținut complex',
            'data': {
                'content': '🤖🔒 INFANT.RO - Powered by Gemini AI\nAnaliza completă pentru produsul XYZ',
                'author': {'username': 'webhook_user', 'is_bot': False}
            },
            'should_ignore': True,
            'description': 'Orice mesaj cu 🤖🔒 trebuie ignorat indiferent de conținut'
        },
        {
            'name': 'Mesaj cu prefix bot normal',
            'data': {
                'content': '🤖 Răspuns automat (fără protecție anti-buclă)',
                'author': {'username': 'user456', 'is_bot': False}
            },
            'should_ignore': True,
            'description': 'Mesajele cu prefix 🤖 trebuie tot ignorate'
        },
        {
            'name': 'Mesaj de la bot real Discord',
            'data': {
                'content': 'Notificare automată',
                'author': {'username': 'infant_products', 'is_bot': True}
            },
            'should_ignore': True,
            'description': 'Bot-urile Discord trebuie ignorate'
        }
    ]
    
    print("🔒 Test Anti-Loop pentru Discord Bot")
    print("=" * 70)
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        result = filter.should_ignore_message(test['data'])
        success = result == test['should_ignore']
        
        if success:
            passed += 1
        
        status_icon = "✅" if success else "❌"
        ignore_text = "IGNORAT" if result else "PROCESAT"
        expected_text = "IGNORAT" if test['should_ignore'] else "PROCESAT"
        
        print(f"{status_icon} Test {i}/{total}: {test['name']}")
        print(f"   📝 Conținut: {test['data']['content'][:60]}...")
        print(f"   👤 Autor: {test['data']['author']['username']} (bot: {test['data']['author']['is_bot']})")
        print(f"   🎯 Așteptat: {expected_text}")
        print(f"   📊 Rezultat: {ignore_text}")
        print(f"   💡 {test['description']}")
        print()
    
    print("=" * 70)
    success_rate = (passed / total) * 100
    print(f"📈 Rezultate: {passed}/{total} teste trecute ({success_rate:.1f}%)")
    
    if passed == total:
        print("🎉 TOATE TESTELE AU TRECUT! Funcționalitatea anti-buclă funcționează corect.")
    else:
        print(f"⚠️ {total - passed} teste au eșuat. Verifică implementarea.")
    
    # Use pytest assertion
    assert passed == total, f"Only {passed}/{total} tests passed"

def test_webhook_anti_loop_simulation():
    """Simulează un webhook cu header X-Source: n8n-automation"""
    print("\n🌐 Test Simulare Webhook Anti-Loop")
    print("=" * 50)
    
    # Simulăm data care ar veni de la webhook
    webhook_data = {
        "action": "send_message",
        "channel_id": 123456789,
        "content": "Test mesaj de la n8n automation"
    }
    
    # Simulăm header-ul
    headers = {
        "X-Source": "n8n-automation",
        "Content-Type": "application/json"
    }
    
    print("📤 Simulare request webhook:")
    print(f"   • Header X-Source: {headers.get('X-Source')}")
    print(f"   • Content: {webhook_data['content']}")
    
    # Testăm ce s-ar întâmpla cu conținutul
    content = webhook_data['content']
    is_n8n_automation = headers.get('X-Source', '').lower() == 'n8n-automation'
    
    if is_n8n_automation and not content.startswith('🤖🔒'):
        modified_content = f"🤖🔒 {content}"
        print(f"✅ Prefix anti-buclă adăugat: {modified_content}")
    else:
        modified_content = content
        print(f"ℹ️ Conținut rămas neschimbat: {modified_content}")
    
    # Testăm dacă mesajul modificat ar fi filtrat
    filter = MessageFilter()
    test_message = {
        'content': modified_content,
        'author': {'username': 'webhook_user', 'is_bot': False}
    }
    would_ignore = filter.should_ignore_message(test_message)
    print(f"🔍 Mesajul modificat ar fi: {'IGNORAT' if would_ignore else 'PROCESAT'}")
    
    if is_n8n_automation and would_ignore:
        print("✅ Perfect! Mesajul cu prefix anti-buclă este corect filtrat.")
    elif not is_n8n_automation and not would_ignore:
        print("✅ Corect! Mesajul normal nu este filtrat.")
    else:
        print("❌ Eroare în logica anti-buclă!")
    
    # Use pytest assertion
    result = (is_n8n_automation and would_ignore) or (not is_n8n_automation and not would_ignore)
    assert result, "Anti-loop logic failed"

def main():
    """Rulează toate testele anti-loop"""
    print("🚀 Începe testarea funcționalității anti-buclă\n")
    
    # Test 1: Filtrarea mesajelor cu prefix
    test1_result = test_anti_loop_prefix()
    
    # Test 2: Simularea webhook-ului
    test2_result = test_webhook_anti_loop_simulation()
    
    print("\n" + "=" * 70)
    print("📋 SUMAR FINAL:")
    print(f"   🔒 Test filtrare prefix: {'✅ TRECUT' if test1_result else '❌ EȘUAT'}")
    print(f"   🌐 Test simulare webhook: {'✅ TRECUT' if test2_result else '❌ EȘUAT'}")
    
    if test1_result and test2_result:
        print("\n🎉 TOATE TESTELE ANTI-LOOP AU TRECUT!")
        print("✅ Sistemul este pregătit să prevină buclele de mesaje.")
        return True
    else:
        print("\n⚠️ UNELE TESTE AU EȘUAT!")
        print("❌ Verifică implementarea anti-loop înainte de deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
