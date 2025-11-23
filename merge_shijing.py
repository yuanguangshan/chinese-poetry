import json
import os

shijing_file = '/Users/ygs/chinese-poetry/诗经/shijing.json'
songci_file = '/Users/ygs/yuangs/pages/songci.json'

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

print("Loading files...")
shijing_data = load_json(shijing_file)
songci_data = load_json(songci_file)

print(f"Loaded {len(shijing_data)} poems from Shijing.")
print(f"Loaded {len(songci_data)} poems from Songci.")

converted_shijing = []
for poem in shijing_data:
    new_poem = {
        "author": "诗经",
        "paragraphs": poem.get("content", []),
        "rhythmic": poem.get("title", ""),
        "tags": ["诗经"]
    }
    
    # Add chapter and section to tags if they exist
    if poem.get("chapter"):
        new_poem["tags"].append(poem["chapter"])
    if poem.get("section"):
        new_poem["tags"].append(poem["section"])
        
    converted_shijing.append(new_poem)

# Check for duplicates before appending? 
# The user asked to "append", implying we should just add them.
# But it's good practice to avoid exact duplicates if they already exist (unlikely for Shijing in Songci file, but possible if run multiple times).
# Let's check if "诗经" entries already exist to avoid double insertion if script is run twice.

existing_shijing_count = sum(1 for p in songci_data if "诗经" in p.get("tags", []))
if existing_shijing_count > 0:
    print(f"Warning: Found {existing_shijing_count} existing Shijing poems in target file.")
    # For now, I will append anyway as per instruction, but maybe I should filter?
    # Let's filter out if the exact same title and author "诗经" exists.
    
    existing_titles = set(p.get("rhythmic") for p in songci_data if p.get("author") == "诗经")
    
    to_add = []
    for p in converted_shijing:
        if p["rhythmic"] not in existing_titles:
            to_add.append(p)
        else:
            # Optional: update existing? No, just skip for now to be safe.
            pass
            
    print(f"Adding {len(to_add)} new Shijing poems (skipped {len(converted_shijing) - len(to_add)} duplicates).")
    songci_data.extend(to_add)
else:
    print(f"Adding all {len(converted_shijing)} Shijing poems.")
    songci_data.extend(converted_shijing)

print(f"Total poems after merge: {len(songci_data)}")
save_json(songci_file, songci_data)
