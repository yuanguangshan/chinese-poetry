import json
import os

source_path = '/Users/ygs/chinese-poetry/纳兰性德/纳兰性德诗集.json'
target_path = '/Users/ygs/yuangs/pages/songci.json'

def process_nalan():
    # Read source
    with open(source_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    
    # Transform
    converted_data = []
    for item in source_data:
        new_item = {
            "author": item.get('author', '纳兰性德'),
            "paragraphs": item.get('para', []),
            "rhythmic": item.get('title', ''),
            "tags": ["纳兰性德诗集"]
        }
        converted_data.append(new_item)
    
    # Read target
    if os.path.exists(target_path):
        with open(target_path, 'r', encoding='utf-8') as f:
            target_data = json.load(f)
    else:
        target_data = []
    
    # Merge
    initial_count = len(target_data)
    target_data.extend(converted_data)
    final_count = len(target_data)
    
    # Write back
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(target_data, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(converted_data)} poems from {source_path}")
    print(f"Appended to {target_path}")
    print(f"Total poems: {initial_count} -> {final_count}")

if __name__ == "__main__":
    process_nalan()
