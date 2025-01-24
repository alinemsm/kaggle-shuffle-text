def sort_words(text):
    # Define stop words
    stop_words = {'and', 'as', 'from', 'have', 'in', 'is', 'it', 'not', 'of', 
                  'that', 'the', 'to', 'we', 'with', 'you'}
    
    # Split text into words
    original_words = text.lower().split()
    original_count = len(original_words)
    
    # Count word frequencies
    word_freq = {}
    for word in original_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Separate into stop words and other words (preserving frequency)
    stops = []
    others = []
    
    # Add stop words with their frequencies
    for word in sorted(word_freq.keys()):
        if word in stop_words:
            stops.extend([word] * word_freq[word])
        else:
            others.extend([word] * word_freq[word])
    
    # Combine and join into text
    sorted_words = stops + others
    result = ' '.join(sorted_words)
    
    # Verify word count
    final_count = len(sorted_words)
    if final_count != original_count:
        print(f"WARNING: Word count mismatch! Original: {original_count}, Final: {final_count}")
    else:
        print(f"Word count verified: {original_count} words")
        
    return result

# Test text
text = "toy of season unwrap holiday puzzle joy peace cheer wish greeting carol sing wonder dream yuletide doll cookie angel star reindeer merry holly milk kaggle and of to as from is have advent candle card stocking snowglobe game night that it chocolate gingerbread decorations ornament scrooge jingle sleigh workshop polar wreath gifts wrapping paper peppermint the magi poinsettia eat sleep drive naughty visit and nice mistletoe elf workshop ornament in the chimney fireplace candy fruitcake beard hohoho nutcracker bow relax eggnog cheer we not the grinch bake walk jump hope you family laugh believe give night with chimney fireplace and"

result = sort_words(text)
print(result)