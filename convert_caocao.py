import json
import os

source_path = '/Users/ygs/chinese-poetry/曹操诗集/caocao.json'
target_path = '/Users/ygs/yuangs/pages/caocao.json'

def convert():
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    for item in data:
        new_item = {
            "author": "曹操",
            "paragraphs": item['paragraphs'],
            "rhythmic": item['title'],
            "tags": ["曹操诗集"]
        }
        new_data.append(new_item)

    # Ensure target directory exists
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    print(f"Converted {len(data)} poems to {target_path}")

if __name__ == "__main__":
    convert()
