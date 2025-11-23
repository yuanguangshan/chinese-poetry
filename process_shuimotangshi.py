import json
import os

def process_shuimotangshi(source_path, target_path):
    """
    Converts shuimotangshi.json to the target format and merges into tangshi.json.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source file not found: {source_path}")
        return

    if not os.path.exists(target_path):
        print(f"Error: Target file not found: {target_path}")
        return

    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
        
        with open(target_path, 'r', encoding='utf-8') as f:
            target_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    converted_poems = []
    for entry in source_data:
        # Map fields
        author = entry.get("author", "")
        title = entry.get("title", "")
        paragraphs = entry.get("paragraphs", [])
        prologue = entry.get("prologue", "")
        
        # Construct new entry
        new_entry = {
            "author": author,
            "paragraphs": paragraphs,
            "rhythmic": title,
            "tags": ["唐诗", "水墨唐诗"],
            "desc": prologue
        }
        converted_poems.append(new_entry)

    # Merge
    target_data.extend(converted_poems)

    # Write back to target file
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(target_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully merged {len(converted_poems)} poems from {source_path} into {target_path}")
    except Exception as e:
        print(f"Error writing to target file: {e}")

if __name__ == "__main__":
    source_file = "/Users/ygs/chinese-poetry/水墨唐诗/shuimotangshi.json"
    target_file = "/Users/ygs/yuangs/pages/tangshi.json"
    process_shuimotangshi(source_file, target_file)
