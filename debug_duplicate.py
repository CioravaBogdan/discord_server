import re

def test_duplicate_patterns():
    """Test pentru a vedea de ce regex-ul pentru duplicate eșuează"""
    
    content = "salut, cum merge?"
      duplicate_patterns = [
        r"(\b\w{3,}\b)\s+\1",  # Repeated words (3+ chars)
        r"^(.{10,})\s+\1",  # Repeated longer phrases (10+ chars)
        r"^(.{1,5})\1{4,}",  # Repeated short sequences (4+ times)
    ]
    
    print(f"🔍 Testez: '{content}'")
    
    for i, pattern in enumerate(duplicate_patterns, 1):
        print(f"\nPattern {i}: {pattern}")
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            print(f"   ❌ MATCH găsit: {match.groups()}")
            print(f"   📍 Poziție: {match.start()}-{match.end()}")
            print(f"   📝 Match text: '{match.group()}'")
        else:
            print(f"   ✅ Nu se potrivește")

if __name__ == "__main__":
    test_duplicate_patterns()
