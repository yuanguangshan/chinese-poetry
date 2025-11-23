import json

source_file = '/Users/ygs/chinese-poetry/宋词/宋词三百首.json'
target_file = '/Users/ygs/yuangs/pages/songci.json'

def load_poems(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

source_poems = load_poems(source_file)
target_poems = load_poems(target_file)

missing_targets = [
    {"author": "苏轼", "rhythmic": "卜算子"},
    {"author": "宋祁", "rhythmic": "玉楼春"}
]

print("--- Poems in Source (宋词三百首.json) ---")
for target in missing_targets:
    for p in source_poems:
        if p.get('author') == target['author'] and p.get('rhythmic') == target['rhythmic']:
            print(json.dumps(p, ensure_ascii=False, indent=2))

print("\n--- Potential Matches in Target (songci.json) ---")
for target in missing_targets:
    print(f"Searching for {target['author']} - {target['rhythmic']}...")
    found = False
    for p in target_poems:
        if p.get('author') == target['author'] and p.get('rhythmic') == target['rhythmic']:
            print(json.dumps(p, ensure_ascii=False, indent=2))
            found = True
    if not found:
        print("Not found.")
