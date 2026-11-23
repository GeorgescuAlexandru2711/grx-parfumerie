import os
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / 'media' / 'products'
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

PERFUME_IMAGES = {
    'baccarat-rouge-540': 'https://fimgs.net/mdimg/perfume/375x500.39359.jpg',
    'grand-soir': 'https://fimgs.net/mdimg/perfume/375x500.41054.jpg',
    'aventus': 'https://fimgs.net/mdimg/perfume/375x500.9828.jpg',
    'silver-mountain-water': 'https://fimgs.net/mdimg/perfume/375x500.470.jpg',
    'santal-33': 'https://fimgs.net/mdimg/perfume/375x500.12201.jpg',
    'the-noir-29': 'https://fimgs.net/mdimg/perfume/375x500.31858.jpg',
    'angels-share': 'https://fimgs.net/mdimg/perfume/375x500.62615.jpg',
    'black-phantom-memento-mori': 'https://fimgs.net/mdimg/perfume/375x500.43632.jpg',
    'delina': 'https://fimgs.net/mdimg/perfume/375x500.43864.jpg',
    'herod': 'https://fimgs.net/mdimg/perfume/375x500.16939.jpg',
    'tobacco-vanille': 'https://fimgs.net/mdimg/perfume/375x500.1825.jpg',
    'oud-wood': 'https://fimgs.net/mdimg/perfume/375x500.1826.jpg',
    'naxos': 'https://fimgs.net/mdimg/perfume/375x500.30529.jpg',
    'erba-pura': 'https://fimgs.net/mdimg/perfume/375x500.55157.jpg',
    'gypsy-water': 'https://fimgs.net/mdimg/perfume/375x500.3575.jpg',
    'bal-dafrique': 'https://fimgs.net/mdimg/perfume/375x500.6458.jpg',
    'portrait-of-a-lady': 'https://fimgs.net/mdimg/perfume/375x500.10211.jpg',
    'philosykos': 'https://fimgs.net/mdimg/perfume/375x500.3865.jpg',
    'interlude-man': 'https://fimgs.net/mdimg/perfume/375x500.15294.jpg',
    'reflection-man': 'https://fimgs.net/mdimg/perfume/375x500.924.jpg',
    'hacivat': 'https://fimgs.net/mdimg/perfume/375x500.44174.jpg',
    'ani': 'https://fimgs.net/mdimg/perfume/375x500.54785.jpg',
    'gris-charnel': 'https://fimgs.net/mdimg/perfume/375x500.57016.jpg',
    'rouge-smoking': 'https://fimgs.net/mdimg/perfume/375x500.51495.jpg',
    'jazz-club': 'https://fimgs.net/mdimg/perfume/375x500.20541.jpg',
    'by-the-fireplace': 'https://fimgs.net/mdimg/perfume/375x500.31623.jpg',
    'halfeti': 'https://fimgs.net/mdimg/perfume/375x500.31396.jpg',
    'the-tragedy-of-lord-george': 'https://fimgs.net/mdimg/perfume/375x500.40606.jpg',
    'maison-francis-kurkdjian-wardrobe-for-her': 'https://fimgs.net/mdimg/perfume/375x500.39359.jpg',
    'creed-mens-royal-discovery-coffret': 'https://fimgs.net/mdimg/perfume/375x500.9828.jpg',
    'kilian-paris-the-liquors-discovery-miniature-set': 'https://fimgs.net/mdimg/perfume/375x500.62615.jpg',
    'le-labo-classic-discovery-set': 'https://fimgs.net/mdimg/perfume/375x500.12201.jpg',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Downloading {len(PERFUME_IMAGES)} perfume bottle images...")
for slug, url in PERFUME_IMAGES.items():
    dest = MEDIA_DIR / f"{slug}.jpg"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200 and len(res.content) > 1000:
            with open(dest, 'wb') as f:
                f.write(res.content)
            print(f"  [OK] {slug} ({len(res.content)} bytes)")
        else:
            print(f"  [FAIL {res.status_code}] {slug} -> {url}")
    except Exception as e:
        print(f"  [ERROR] {slug}: {e}")

