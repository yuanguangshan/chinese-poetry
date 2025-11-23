import json
import collections

def deduplicate_tangshi(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Original entries: {len(data)}")

    # Group by Author + Title
    merged_data = {}
    
    for poem in data:
        key = (poem.get('author', ''), poem.get('rhythmic', ''))
        
        if key not in merged_data:
            merged_data[key] = poem
        else:
            existing = merged_data[key]
            
            # Merge Tags
            existing_tags = set(existing.get('tags', []))
            new_tags = set(poem.get('tags', []))
            existing['tags'] = list(existing_tags.union(new_tags))
            
            # Keep longer desc
            existing_desc = existing.get('desc', '')
            new_desc = poem.get('desc', '')
            
            # Simple heuristic: keep the one with more characters, assuming it's richer
            # Also prefer one that has HTML tags if the other doesn't, but length usually covers this for poem.xml vs shuimotangshi
            if len(new_desc) > len(existing_desc):
                existing['desc'] = new_desc
            
            # We assume paragraphs are effectively the same or we keep the first one encountered.
            # If we wanted to be stricter, we could check content similarity. 
            # For now, we trust the Author+Title match.

    final_list = list(merged_data.values())
    
    print(f"Deduplicated entries: {len(final_list)}")
    print(f"Removed {len(data) - len(final_list)} duplicates.")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_list, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved to {file_path}")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    deduplicate_tangshi("/Users/ygs/yuangs/pages/tangshi.json")
