import json
import os
try:
    from zhconv import convert
except ImportError:
    print("zhconv not found, please install it using 'pip install zhconv'")
    exit(1)

def to_simplified(text):
    return convert(text, 'zh-cn')

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

target_file = '/Users/ygs/yuangs/pages/songci.json'
songci_data = load_json(target_file)
if songci_data is None:
    songci_data = []

new_entries = []

# 1. Process sanzijing-new.json
sanzijing_new_file = '/Users/ygs/chinese-poetry/蒙学/sanzijing-new.json'
data = load_json(sanzijing_new_file)
if data:
    entry = {
        "author": to_simplified(data.get("author", "王应麟")),
        "rhythmic": to_simplified(data.get("title", "三字经")),
        "paragraphs": [to_simplified(p) for p in data.get("paragraphs", [])],
        "tags": ["蒙学", "三字经", "新版"]
    }
    new_entries.append(entry)
    print("Processed sanzijing-new.json")

# 2. Process sanzijing-traditional.json
sanzijing_trad_file = '/Users/ygs/chinese-poetry/蒙学/sanzijing-traditional.json'
data = load_json(sanzijing_trad_file)
if data:
    entry = {
        "author": to_simplified(data.get("author", "王应麟")),
        "rhythmic": to_simplified(data.get("title", "三字经")),
        "paragraphs": [to_simplified(p) for p in data.get("paragraphs", [])],
        "tags": ["蒙学", "三字经", "传统版"]
    }
    new_entries.append(entry)
    print("Processed sanzijing-traditional.json")

# 3. Process shenglvqimeng.json
shenglv_file = '/Users/ygs/chinese-poetry/蒙学/shenglvqimeng.json'
data = load_json(shenglv_file)
if data:
    main_title = to_simplified(data.get("title", "声律启蒙"))
    author = to_simplified(data.get("author", "车万育"))
    
    # Iterate through volumes (上卷, 下卷)
    for volume in data.get("content", []):
        vol_title = to_simplified(volume.get("title", ""))
        
        # Iterate through chapters (一 东, 二 冬, etc.)
        for chapter in volume.get("content", []):
            chap_title = to_simplified(chapter.get("chapter", ""))
            paragraphs = [to_simplified(p) for p in chapter.get("paragraphs", [])]
            
            entry = {
                "author": author,
                "rhythmic": main_title,
                "paragraphs": paragraphs,
                "tags": ["蒙学", "声律启蒙", vol_title, chap_title]
            }
            new_entries.append(entry)
    print("Processed shenglvqimeng.json")

# Append to songci_data
print(f"Adding {len(new_entries)} new entries.")
songci_data.extend(new_entries)

print(f"Total poems after merge: {len(songci_data)}")
save_json(target_file, songci_data)
