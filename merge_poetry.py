import json
import hashlib
import re

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

def get_content_hash(poem):
    """Generate hash from author + rhythmic + paragraphs for deduplication"""
    author = poem.get('author', '').strip()
    rhythmic = poem.get('rhythmic', '').strip()
    paragraphs = ''.join(poem.get('paragraphs', [])).replace(' ', '').replace('\n', '')
    content = f"{author}|{rhythmic}|{paragraphs}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def infer_theme_tags(poem):
    """Infer theme tags based on content and title"""
    themes = []
    author = poem.get('author', '')
    rhythmic = poem.get('rhythmic', '')
    content = ''.join(poem.get('paragraphs', []))
    
    # 边塞诗
    if any(kw in content or kw in rhythmic for kw in ['关', '塞', '戍', '征', '胡', '羌', '烽火', '长城', '玉门', '阴山', '龙城']):
        themes.append('边塞')
    
    # 田园诗
    if any(kw in content or kw in rhythmic for kw in ['田', '农', '耕', '桑', '麻', '菊', '篱', '归', '隐', '山居', '渔樵']):
        themes.append('田园')
    
    # 送别诗
    if any(kw in content or kw in rhythmic for kw in ['送', '别', '离', '行', '赠', '饯', '征人', '游子', '客']):
        themes.append('送别')
    
    # 思乡诗
    if any(kw in content or kw in rhythmic for kw in ['思', '乡', '故', '归', '家', '月', '梦', '泪', '愁']):
        themes.append('思乡')
    
    # 爱国诗
    if any(kw in content or kw in rhythmic for kw in ['国', '君', '社稷', '天下', '报国', '忠', '义']):
        themes.append('爱国')
    
    # 咏物诗
    if any(kw in rhythmic for kw in ['咏', '题', '赋']):
        themes.append('咏物')
    
    # 山水诗
    if any(kw in content for kw in ['山', '水', '江', '河', '湖', '海', '峰', '岭', '溪', '泉']):
        themes.append('山水')
    
    # 爱情诗
    if any(kw in content for kw in ['相思', '佳人', '美人', '情', '恋', '夫妇', '君子好逑']):
        themes.append('爱情')
    
    # 节日诗
    if any(kw in rhythmic or kw in content for kw in ['清明', '重阳', '中秋', '元夕', '端午', '七夕']):
        themes.append('节日')
    
    return themes

def categorize_poem(poem, source):
    """Add appropriate tags based on source and content"""
    tags = poem.get('tags', [])
    if not isinstance(tags, list):
        tags = [tags] if tags else []
    
    author = poem.get('author', '')
    rhythmic = poem.get('rhythmic', '')
    
    # Pre-Qin authors
    pre_qin_authors = ['屈原', '宋玉', '荀子', '庄子', '孟子', '孔子', '老子', '韩非子']
    # Han dynasty authors
    han_authors = ['司马相如', '卓文君', '刘邦', '项羽', '刘彻']
    # Wei-Jin authors
    weijin_authors = ['曹操', '曹丕', '曹植', '陶渊明', '阮籍', '嵇康', '谢灵运', '鲍照']
    # Tang authors (sample)
    tang_authors = ['李白', '杜甫', '王维', '白居易', '孟浩然', '王昌龄', '李商隐', '杜牧', '刘禹锡', '韩愈', '柳宗元', '元稹', '张继', '王之涣', '贺知章', '骆宾王', '陈子昂']
    # Southern Tang
    southern_tang_authors = ['李煜', '李璟', '冯延巳']
    # Song authors (sample)
    song_authors = ['苏轼', '李清照', '辛弃疾', '柳永', '岳飞', '陆游', '欧阳修', '王安石', '晏殊', '晏几道', '周邦彦', '秦观', '贺铸', '姜夔', '吴文英', '张先', '黄庭坚']
    # Qing authors
    qing_authors = ['纳兰性德', '纳兰容若', '顾贞观', '陈维崧', '朱彝尊']
    # Modern authors
    modern_authors = ['毛泽东']
    
    # Determine dynasty and type
    if '诗经' in tags or author == '诗经':
        if '先秦' not in tags:
            tags.insert(0, '先秦')
        if '诗经' not in tags:
            tags.insert(1, '诗经')
    elif '蒙学' in tags:
        pass  # Keep existing tags
    elif author in pre_qin_authors or '楚辞' in rhythmic or '九歌' in rhythmic or '离骚' in rhythmic:
        if '先秦' not in tags:
            tags.insert(0, '先秦')
        if '楚辞' in rhythmic or '九歌' in rhythmic or '离骚' in rhythmic:
            if '楚辞' not in tags:
                tags.append('楚辞')
    elif author in han_authors:
        if '汉' not in tags:
            tags.insert(0, '汉')
        if '乐府' not in tags:
            tags.append('乐府')
    elif author in weijin_authors:
        if '魏晋' not in tags:
            tags.insert(0, '魏晋')
    elif author in southern_tang_authors:
        if '南唐' not in tags:
            tags.insert(0, '南唐')
        if '词' not in tags:
            tags.append('词')
    elif author in qing_authors:
        if '清' not in tags:
            tags.insert(0, '清')
        if '清词' not in tags:
            tags.append('清词')
    elif author in modern_authors:
        if '现代' not in tags:
            tags.insert(0, '现代')
        if '毛泽东诗词' not in tags:
            tags.append('毛泽东诗词')
    elif source == 'tangshi' or author in tang_authors or '唐诗' in tags:
        if '唐' not in tags and '唐诗' not in tags:
            tags.insert(0, '唐')
        if '唐诗' not in tags:
            tags.insert(1, '唐诗')
        # Infer form from existing type field
        type_field = poem.get('type', '')
        if type_field and type_field not in tags:
            tags.append(type_field)
    elif source == 'songci' or author in song_authors or '宋词' in tags:
        # Default to Song Ci if no other dynasty identified
        if not any(d in tags for d in ['先秦', '汉', '魏晋', '南唐', '唐', '清', '现代']):
            if '宋' not in tags:
                tags.insert(0, '宋')
            if '宋词' not in tags:
                tags.insert(1, '宋词')
    
    # Add theme tags
    theme_tags = infer_theme_tags(poem)
    for theme in theme_tags:
        if theme not in tags:
            tags.append(theme)
    
    poem['tags'] = tags
    return poem

def merge_poetry():
    tangshi_file = '/Users/ygs/yuangs/pages/tangshi.json'
    songci_file = '/Users/ygs/yuangs/pages/songci.json'
    output_file = '/Users/ygs/yuangs/pages/poetry_data.json'
    
    print("Loading files...")
    tangshi_data = load_json(tangshi_file)
    songci_data = load_json(songci_file)
    
    print(f"Loaded {len(tangshi_data)} poems from tangshi.json")
    print(f"Loaded {len(songci_data)} poems from songci.json")
    
    # Track poems by hash for deduplication
    poem_dict = {}
    
    # Process tangshi first (higher priority for Tang poems)
    print("\nProcessing tangshi.json...")
    for poem in tangshi_data:
        poem = categorize_poem(poem, 'tangshi')
        hash_key = get_content_hash(poem)
        poem_dict[hash_key] = poem
    
    # Process songci
    print("Processing songci.json...")
    duplicates = 0
    for poem in songci_data:
        poem = categorize_poem(poem, 'songci')
        hash_key = get_content_hash(poem)
        if hash_key in poem_dict:
            duplicates += 1
            # Keep the one with desc if available
            existing = poem_dict[hash_key]
            if poem.get('desc') and not existing.get('desc'):
                poem_dict[hash_key] = poem
        else:
            poem_dict[hash_key] = poem
    
    print(f"Found {duplicates} duplicates")
    
    # Convert to list
    merged_data = list(poem_dict.values())
    
    # Sort by dynasty order
    dynasty_order = {
        '先秦': 0,
        '汉': 1,
        '魏晋': 2,
        '南北朝': 3,
        '隋': 4,
        '唐': 5,
        '五代': 6,
        '南唐': 6,
        '宋': 7,
        '元': 8,
        '明': 9,
        '清': 10,
        '现代': 11
    }
    
    def get_sort_key(poem):
        tags = poem.get('tags', [])
        for dynasty in dynasty_order:
            if dynasty in tags:
                return dynasty_order[dynasty]
        return 999
    
    merged_data.sort(key=get_sort_key)
    
    print(f"\nTotal poems after merge: {len(merged_data)}")
    
    # Statistics
    print("\n=== Statistics ===")
    dynasty_counts = {}
    for poem in merged_data:
        tags = poem.get('tags', [])
        dynasty = None
        for tag in tags:
            if tag in dynasty_order:
                dynasty = tag
                break
        if dynasty:
            dynasty_counts[dynasty] = dynasty_counts.get(dynasty, 0) + 1
    
    for dynasty in sorted(dynasty_counts.keys(), key=lambda x: dynasty_order.get(x, 999)):
        print(f"{dynasty}: {dynasty_counts[dynasty]}")
    
    save_json(output_file, merged_data)
    return merged_data

if __name__ == '__main__':
    merge_poetry()
