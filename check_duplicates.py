import json
import collections

def check_duplicates(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Total entries: {len(data)}")

    # Check by Author + Title
    author_title_counts = collections.defaultdict(list)
    for i, poem in enumerate(data):
        key = (poem.get('author', ''), poem.get('rhythmic', ''))
        author_title_counts[key].append(i)

    duplicates_at = {k: v for k, v in author_title_counts.items() if len(v) > 1}
    
    print(f"\nPotential duplicates by Author + Title: {len(duplicates_at)} groups")
    for (author, title), indices in list(duplicates_at.items())[:10]: # Show first 10
        print(f"  - {author} - {title}: {len(indices)} entries (Indices: {indices})")

    # Check by Content (first paragraph)
    content_counts = collections.defaultdict(list)
    for i, poem in enumerate(data):
        paras = poem.get('paragraphs', [])
        if paras:
            key = paras[0] # Use first paragraph as key
            content_counts[key].append(i)
    
    duplicates_content = {k: v for k, v in content_counts.items() if len(v) > 1}
    print(f"\nPotential duplicates by First Paragraph: {len(duplicates_content)} groups")
    for content, indices in list(duplicates_content.items())[:10]:
        print(f"  - {content[:20]}...: {len(indices)} entries (Indices: {indices})")

    # Check for exact full duplicates (ignoring tags/desc which might differ)
    full_content_counts = collections.defaultdict(list)
    for i, poem in enumerate(data):
        # Create a hashable representation of the core content
        paras = tuple(poem.get('paragraphs', []))
        author = poem.get('author', '')
        title = poem.get('rhythmic', '')
        key = (author, title, paras)
        full_content_counts[key].append(i)

    duplicates_full = {k: v for k, v in full_content_counts.items() if len(v) > 1}
    print(f"\nExact duplicates (Author + Title + Paragraphs): {len(duplicates_full)} groups")
    
    return len(duplicates_full)

if __name__ == "__main__":
    check_duplicates("/Users/ygs/yuangs/pages/tangshi.json")
