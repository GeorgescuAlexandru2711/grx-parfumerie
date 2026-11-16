import os
import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grx_project.settings')
import django
django.setup()

from apps.catalog.models import Product

MEDIA_DIR = Path('media') / 'products'

# Map title keyword or identifier to downloaded image
IMAGE_MAP = {
    'Baccarat Rouge 540': 'baccarat-rouge-540.jpg',
    'Grand Soir': 'grand-soir.jpg',
    'Aventus': 'aventus.jpg',
    'Silver Mountain Water': 'silver-mountain-water.jpg',
    'Santal 33': 'santal-33.jpg',
    'Thé Noir 29': 'the-noir-29.jpg',
    'Angels’ Share': 'angels-share.jpg',
    'Black Phantom': 'black-phantom-memento-mori.jpg',
    'Delina': 'delina.jpg',
    'Herod': 'herod.jpg',
    'Tobacco Vanille': 'tobacco-vanille.jpg',
    'Oud Wood': 'oud-wood.jpg',
    'Naxos': 'naxos.jpg',
    'Erba Pura': 'erba-pura.jpg',
    'Gypsy Water': 'gypsy-water.jpg',
    'Bal d’Afrique': 'bal-dafrique.jpg',
    'Portrait of a Lady': 'portrait-of-a-lady.jpg',
    'Philosykos': 'philosykos.jpg',
    'Interlude Man': 'interlude-man.jpg',
    'Reflection Man': 'reflection-man.jpg',
    'Hacivat': 'hacivat.jpg',
    'Ani': 'ani.jpg',
    'Gris Charnel': 'gris-charnel.jpg',
    'Rouge Smoking': 'rouge-smoking.jpg',
    'Jazz Club': 'jazz-club.jpg',
    'By the Fireplace': 'by-the-fireplace.jpg',
    'Halfeti': 'halfeti.jpg',
    'The Tragedy of Lord George': 'the-tragedy-of-lord-george.jpg',
    'Wardrobe for Her': 'maison-francis-kurkdjian-wardrobe-for-her.jpg',
    'Royal Discovery Coffret': 'creed-mens-royal-discovery-coffret.jpg',
    'The Liquors Discovery': 'kilian-paris-the-liquors-discovery-miniature-set.jpg',
    'Classic Discovery Set': 'le-labo-classic-discovery-set.jpg',
}

updated = 0
for product in Product.objects.all():
    matched_img = None
    for key, filename in IMAGE_MAP.items():
        if key.lower() in product.title.lower():
            matched_img = filename
            break
    
    if matched_img:
        source_file = MEDIA_DIR / matched_img
        target_name = f"{product.slug}.jpg"
        target_file = MEDIA_DIR / target_name

        if source_file.exists():
            if source_file != target_file:
                shutil.copyfile(source_file, target_file)
            product.image = f"products/{target_name}"
            product.image_url = f"/media/products/{target_name}"
            product.save(update_fields=['image', 'image_url'])
            updated += 1
            print(f"  [OK] {product.title} -> {product.image.url}")
        else:
            print(f"  [MISSING FILE] {matched_img} for {product.title}")
    else:
        print(f"  [NO MATCH] {product.title}")

print(f"\nSuccessfully attached accurate bottle photos to {updated} out of {Product.objects.count()} perfumes!")
