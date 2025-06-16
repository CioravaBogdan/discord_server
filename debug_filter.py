from message_filters import MessageFilter

def debug_filter_message():
    """Debug specific pentru a vedea de ce mesajul normal este filtrat"""
    filter = MessageFilter()
    
    # Mesajul care eșuează
    test_message = {
        'content': 'Salut, cum merge?',
        'author': {'username': 'user123', 'is_bot': False}
    }
    
    content = test_message.get('content', '').lower().strip()
    author = test_message.get('author', {})
    author_name = author.get('username', '').lower()
    display_name = author.get('display_name', '').lower()
    is_bot = author.get('is_bot', False)
    
    print(f"🔍 Debug mesaj: '{content}'")
    print(f"👤 Autor: {author_name} (bot: {is_bot})")
    print()
    
    # 1. Check bot author
    print(f"1. Este bot: {is_bot}")
    if is_bot:
        print("   ❌ FILTRAT: Author este bot")
        return
    
    # 2. Check known bot names
    for bot_name in filter.known_bots:
        if bot_name in author_name or bot_name in display_name:
            print(f"   ❌ FILTRAT: Bot cunoscut - {bot_name}")
            return
    print("   ✅ Nu este bot cunoscut")
    
    # 3. Check bot prefixes
    for prefix in filter.bot_prefixes:
        if content.startswith(prefix.lower()):
            print(f"   ❌ FILTRAT: Prefix bot - {prefix}")
            return
    print("   ✅ Nu are prefix bot")
    
    # 4. Check automated message patterns
    import re
    for pattern in filter.bot_patterns:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            print(f"   ❌ FILTRAT: Pattern bot - {pattern}")
            return
    print("   ✅ Nu se potrivește cu pattern-uri bot")
    
    # 5. Check n8n indicators
    for indicator in filter.n8n_indicators:
        if indicator.lower() in content:
            print(f"   ❌ FILTRAT: Indicator n8n - {indicator}")
            return
    print("   ✅ Nu conține indicatori n8n")
    
    # 6. Check duplicate patterns
    if filter._is_duplicate_pattern(content):
        print("   ❌ FILTRAT: Pattern duplicat")
        return
    print("   ✅ Nu este pattern duplicat")
    
    # 7. Check system message
    if filter._is_system_message(test_message):
        print("   ❌ FILTRAT: Mesaj sistem")
        return
    print("   ✅ Nu este mesaj sistem")
    
    print("\n✅ Mesajul NU TREBUIE să fie filtrat!")

if __name__ == "__main__":
    debug_filter_message()
