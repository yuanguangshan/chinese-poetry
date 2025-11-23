import xml.etree.ElementTree as ET
import json
import os

def convert_poem_xml_to_json(xml_path, json_path):
    """
    Converts poem.xml to tangshi.json format.
    """
    if not os.path.exists(xml_path):
        print(f"Error: File not found: {xml_path}")
        return

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    poems = []
    
    # Iterate through 'node' elements
    for node in root.findall('node'):
        try:
            title = node.find('title').text if node.find('title') is not None else ""
            author = node.find('auth').text if node.find('auth') is not None else ""
            poem_type = node.find('type').text if node.find('type') is not None else ""
            content_raw = node.find('content').text if node.find('content') is not None else ""
            desc = node.find('desc').text if node.find('desc') is not None else ""

            # Clean content and split into paragraphs
            # The content often has <br /> or <br> tags. 
            # We'll replace <br /> and <br> with a placeholder, then split.
            # Also remove any leading/trailing whitespace.
            
            if content_raw:
                # Normalize line breaks
                content_clean = content_raw.replace("<br />", "\n").replace("<br>", "\n")
                paragraphs = [line.strip() for line in content_clean.split('\n') if line.strip()]
            else:
                paragraphs = []

            # Construct tags
            tags = ["唐诗"]
            if poem_type:
                tags.append(poem_type)

            poem_entry = {
                "author": author,
                "paragraphs": paragraphs,
                "rhythmic": title,
                "tags": tags,
                "desc": desc
            }
            
            poems.append(poem_entry)

        except Exception as e:
            print(f"Error processing a node: {e}")
            continue

    # Write to JSON file
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(poems, f, ensure_ascii=False, indent=2)
        print(f"Successfully converted {len(poems)} poems to {json_path}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    xml_file = "/Users/ygs/yuangs/pages/poem.xml"
    json_file = "/Users/ygs/yuangs/pages/tangshi.json"
    convert_poem_xml_to_json(xml_file, json_file)
