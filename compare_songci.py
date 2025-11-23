import json

def get_poem_id(poem):
    # Create a unique signature for the poem
    # Using author, rhythmic, and content
    author = poem.get('author', '').strip()
    rhythmic = poem.get('rhythmic', '').strip()
    # Normalize paragraphs: join and strip whitespace
    paragraphs = ''.join(poem.get('paragraphs', [])).replace(' ', '').replace('\n', '')
    return f"{author}|{rhythmic}|{paragraphs}"

def load_poems(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

source_file = '/Users/ygs/chinese-poetry/宋词/宋词三百首.json'
target_file = '/Users/ygs/yuangs/pages/songci.json'

print(f"Loading source: {source_file}")
source_poems = load_poems(source_file)
print(f"Loading target: {target_file}")
target_poems = load_poems(target_file)

target_ids = set(get_poem_id(p) for p in target_poems)

missing_poems = []
for poem in source_poems:
    pid = get_poem_id(poem)
    if pid not in target_ids:
        missing_poems.append(poem)

print(f"Total poems in source: {len(source_poems)}")
print(f"Total poems in target: {len(target_poems)}")
print(f"Missing poems count: {len(missing_poems)}")

if missing_poems:
    print("\nMissing Poems:")
    for p in missing_poems:
        print(f"- {p.get('author')} 《{p.get('rhythmic')}》")
else:
    print("All poems from source are present in target.")
