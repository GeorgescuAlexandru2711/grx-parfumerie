from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Brand, FragranceFamily, Product, ProductVariant

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database with 30+ curated fragrances, categories, brands, variants, and demo accounts.'

    def handle(self, *args, **options):
        self.stdout.write("==> Starting GrX Parfums Database Seeding...")

        # 1. Create Default Users (Argon2 hashed)
        admin_user, created = User.objects.get_or_create(
            email='admin@grxparfums.ro',
            defaults={
                'first_name': 'Alexandru',
                'last_name': 'Admin',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
                'phone_number': '+40 721 000 001',
                'city': 'Bucharest',
                'county': 'Sector 1',
            }
        )
        if created:
            admin_user.set_password('GrXadmin2026!')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("  [+] Created Admin: admin@grxparfums.ro / GrXadmin2026!"))

        demo_customer, created = User.objects.get_or_create(
            email='alex@example.com',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Georgescu',
                'role': User.Role.CUSTOMER,
                'phone_number': '+40 722 111 222',
                'address_line1': 'Calea Victoriei 120, Ap. 14',
                'city': 'Bucharest',
                'county': 'Sector 1',
                'postal_code': '010074',
            }
        )
        if created:
            demo_customer.set_password('CustomerPass2026!')
            demo_customer.save()
            self.stdout.write(self.style.SUCCESS("  [+] Created Demo Customer: alex@example.com / CustomerPass2026!"))

        # 2. Categories (4 primary categories as per Slide 3)
        cat_data = [
            ('Women', 'women', 'Sophisticated, radiant, and intoxicating feminine compositions.'),
            ('Men', 'men', 'Charismatic, refined, and powerful masculine olfactory statements.'),
            ('Unisex', 'unisex', 'Genderless artistic masterworks transcending traditional boundaries.'),
            ('Gift sets', 'gift-sets', 'Curated luxury discovery coffrets and complete fragrance rituals.'),
        ]
        categories = {}
        for name, slug, desc in cat_data:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'slug': slug, 'description': desc})
            categories[slug] = cat

        # 3. Fragrance Families
        fam_data = [
            ('Woody', 'woody', 'Distinguished cedarwood, sandalwood, vetiver, and smoky agarwood (oud).'),
            ('Oriental & Amber', 'oriental-amber', 'Sensual warm resins, vanilla, golden ambergris, and exotic spices.'),
            ('Fresh & Citrus', 'fresh-citrus', 'Zesty Italian bergamot, crisp ocean breezes, sparkling citrus, and neroli.'),
            ('Floral', 'floral', 'Opulent May roses, night-blooming jasmine, tuberose, and delicate iris.'),
            ('Gourmand', 'gourmand', 'Decadent tonka bean, roasted almonds, dark chocolate, and spiced honey.'),
            ('Leather & Smoke', 'leather-smoke', 'Birch tar, saddle leather, rich Cuban tobacco, and sacred incense.'),
        ]
        families = {}
        for name, slug, desc in fam_data:
            fam, _ = FragranceFamily.objects.get_or_create(name=name, defaults={'slug': slug, 'description': desc})
            families[slug] = fam

        # 4. Brands
        brand_data = [
            ('Maison Francis Kurkdjian', 'mfk', 'France'),
            ('Creed', 'creed', 'France'),
            ('Le Labo', 'le-labo', 'USA'),
            ('Kilian Paris', 'kilian', 'France'),
            ('Parfums de Marly', 'pdm', 'France'),
            ('Tom Ford Private Blend', 'tom-ford', 'USA'),
            ('Xerjoff', 'xerjoff', 'Italy'),
            ('Byredo', 'byredo', 'Sweden'),
            ('Éditions de Parfums Frédéric Malle', 'frederic-malle', 'France'),
            ('Diptyque', 'diptyque', 'France'),
            ('Amouage', 'amouage', 'Oman'),
            ('Nishane', 'nishane', 'Turkey'),
            ('BDK Parfums', 'bdk', 'France'),
            ('Maison Margiela REPLICA', 'replica', 'France'),
            ('Penhaligon’s', 'penhaligons', 'UK'),
        ]
        brands = {}
        for name, slug, country in brand_data:
            b, _ = Brand.objects.get_or_create(name=name, defaults={'slug': slug, 'origin_country': country})
            brands[slug] = b

        # 5. Curated Fragrances (32 distinct luxury fragrances)
        catalog = [
            # 1
            {
                'title': 'Baccarat Rouge 540',
                'brand': 'mfk',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'Luminous and intense, settling on the skin like an amber floral breeze.',
                'desc': 'Baccarat Rouge 540 caresses the skin like an amber and woody floral whisper. A graphic and highly condensed signature born of the encounter between Maison Francis Kurkdjian and Baccarat.',
                'top': 'Bitter Almond, Saffron from saffron crocus',
                'heart': 'Egyptian Jasmine Grandiflorum, Cedarwood',
                'base': 'Ambergris Accord, Woody Musk',
                'image': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'MFK-BR540-10', Decimal('220.00'), 15, False),
                    ('70ml Eau de Parfum', 70, 'MFK-BR540-70', Decimal('1180.00'), 12, True),
                    ('200ml Grand Presentation', 200, 'MFK-BR540-200', Decimal('2250.00'), 6, False),
                ]
            },
            # 2
            {
                'title': 'Grand Soir',
                'brand': 'mfk',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'A radiant Parisian evening wrapped in golden warmth and velvety amber.',
                'desc': 'Dress in your finest attire and polish your look. Experience the luminous energy and nocturnal magic of a grand evening in the City of Light.',
                'top': 'Spanish Labdanum, Lavender',
                'heart': 'Benzoin from Siam',
                'base': 'Brazilian Tonka Bean, Vanilla Amber Accord',
                'image': 'https://images.unsplash.com/photo-1547887537-6158d64c35b3?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'MFK-GS-10', Decimal('190.00'), 10, False),
                    ('70ml Eau de Parfum', 70, 'MFK-GS-70', Decimal('990.00'), 8, True),
                ]
            },
            # 3
            {
                'title': 'Aventus',
                'brand': 'creed',
                'category': 'men',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'Sensual, audacious, and contemporary: celebrating strength and success.',
                'desc': 'The exceptional Aventus was inspired by the dramatic life of a historic emperor, celebrating strength, power and success. Introduced in 2010 and crafted by the deft hand of Olivier Creed.',
                'top': 'Lemon, Pink Pepper, Italian Apple, Bergamot, Blackcurrant',
                'heart': 'Pineapple, Jasmine, Indonesian Patchouli',
                'base': 'Birch, Ambergris, Cedarwood, Oakmoss, Musk',
                'image': 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'CRD-AV-10', Decimal('240.00'), 18, False),
                    ('50ml Eau de Parfum', 50, 'CRD-AV-50', Decimal('1290.00'), 10, False),
                    ('100ml Eau de Parfum', 100, 'CRD-AV-100', Decimal('1790.00'), 14, True),
                ]
            },
            # 4
            {
                'title': 'Silver Mountain Water',
                'brand': 'creed',
                'category': 'unisex',
                'family': 'fresh-citrus',
                'conc': Product.Concentration.EDP,
                'short': 'Crisp, icy alpine freshness inspired by sparkling Swiss mountain streams.',
                'desc': 'The invigorating freshness of Silver Mountain Water captures the purity of the Swiss Alps, with notes of milky blackcurrant and cooling green tea.',
                'top': 'Bergamot, Mandarin Orange, Neroli',
                'heart': 'Green Tea, Blackcurrant Bud',
                'base': 'Sandalwood, Musk, Petitgrain, Galbanum',
                'image': 'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('10ml Travel Discovery', 10, 'CRD-SMW-10', Decimal('220.00'), 8, False),
                    ('100ml Eau de Parfum', 100, 'CRD-SMW-100', Decimal('1650.00'), 7, True),
                ]
            },
            # 5
            {
                'title': 'Santal 33',
                'brand': 'le-labo',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'An intoxicating icon of smoky Australian sandalwood and cardamom.',
                'desc': 'Do you remember the old Marlboro advertisements? Santal 33 touches the vast and wild universality of this dream: an open fire, the soft drift of smoke, where sensuality rises.',
                'top': 'Violet Accord, Cardamom',
                'heart': 'Iris, Papyrus, Ambrox',
                'base': 'Cedarwood, Leather, Sandalwood',
                'image': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('15ml Travel Discovery', 15, 'LL-S33-15', Decimal('320.00'), 14, False),
                    ('50ml Eau de Parfum', 50, 'LL-S33-50', Decimal('980.00'), 9, False),
                    ('100ml Eau de Parfum', 100, 'LL-S33-100', Decimal('1490.00'), 11, True),
                ]
            },
            # 6
            {
                'title': 'Thé Noir 29',
                'brand': 'le-labo',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'An ode to black tea leaves, wrapped in fig freshness and dark cedar.',
                'desc': 'Thé Noir 29 is an ode to the noble leaf and the craft that surrounds it. It combines depth and freshness, softness and strength through permanent oscillation.',
                'top': 'Fig, Bay Leaf, Bergamot',
                'heart': 'Cedar, Vetiver, Musk',
                'base': 'Black Tea Leaf, Tobacco, Hay',
                'image': 'https://images.unsplash.com/photo-1615397349754-cfa2066a298e?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('50ml Eau de Parfum', 50, 'LL-TN29-50', Decimal('980.00'), 8, True),
                    ('100ml Eau de Parfum', 100, 'LL-TN29-100', Decimal('1490.00'), 5, False),
                ]
            },
            # 7
            {
                'title': 'Angels’ Share',
                'brand': 'kilian',
                'category': 'unisex',
                'family': 'gourmand',
                'conc': Product.Concentration.EDP,
                'short': 'Hennessy cognac essence, cinnamon bark, oak absolute, and praline.',
                'desc': 'Much like a Master Blender who combines eaux-de-vie in exceptional proportions, Kilian Hennessy creates his most personal fragrance yet, inspired by his heritage.',
                'top': 'Cognac Oil, Nutmeg',
                'heart': 'Cinnamon Bark, Oak Absolute, Tonka Bean',
                'base': 'Praline, Vanilla, Creamy Sandalwood',
                'image': 'https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'KLN-AS-10', Decimal('260.00'), 16, False),
                    ('50ml Crystal Carafe', 50, 'KLN-AS-50', Decimal('1150.00'), 9, True),
                ]
            },
            # 8
            {
                'title': 'Black Phantom "Memento Mori"',
                'brand': 'kilian',
                'category': 'unisex',
                'family': 'gourmand',
                'conc': Product.Concentration.EDP,
                'short': 'Dark roasted coffee, Martinique rum, cyanide-almond, and cane sugar.',
                'desc': 'An intoxicating pirate brew: roasted Ethiopian coffee laced with dark Martinique rum and bittersweet almond, resting on a bed of vetiver and cane sugar.',
                'top': 'Martinique Rum Accord, Sugar Cane',
                'heart': 'Dark Roasted Coffee, Bitter Almond, Heliotrope',
                'base': 'Java Vetiver, Sandalwood',
                'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('50ml Eau de Parfum', 50, 'KLN-BP-50', Decimal('1190.00'), 6, True),
                ]
            },
            # 9
            {
                'title': 'Delina',
                'brand': 'pdm',
                'category': 'women',
                'family': 'floral',
                'conc': Product.Concentration.EDP,
                'short': 'Sensual floral bouquet sculpted around Damascena rose and crisp lychee.',
                'desc': 'Delina is a tribute to luminous and sensual femininity. A charming and firmly modern bouquet composed around Turkish rose, lily of the valley, and peachy lychee.',
                'top': 'Lychee, Rhubarb, Bergamot, Nutmeg',
                'heart': 'Turkish Rose, Peony, Musk, Petalia, Vanilla',
                'base': 'Cashmeran, Cedarwood, Incense, Haitian Vetiver',
                'image': 'https://images.unsplash.com/photo-1582211594533-268f4f1edcb9?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'PDM-DEL-10', Decimal('210.00'), 20, False),
                    ('75ml Eau de Parfum', 75, 'PDM-DEL-75', Decimal('1290.00'), 11, True),
                ]
            },
            # 10
            {
                'title': 'Herod',
                'brand': 'pdm',
                'category': 'men',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'A royal spectacle of smoky vanilla, cured tobacco leaf, and cinnamon.',
                'desc': 'Herod is personified by its blend of diverse notes, exuding a smoky vanilla scent. This eau de parfum opens on spicy top notes of cinnamon and pepperwood.',
                'top': 'Cinnamon, Pepperwood',
                'heart': 'Tobacco Leaf, Incense, Osmanthus, Labdanum',
                'base': 'Vanilla Pod, Iso E Super, Cedar, Musk, Cypriol',
                'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('10ml Travel Discovery', 10, 'PDM-HER-10', Decimal('190.00'), 9, False),
                    ('125ml Eau de Parfum', 125, 'PDM-HER-125', Decimal('1350.00'), 7, True),
                ]
            },
            # 11
            {
                'title': 'Tobacco Vanille',
                'brand': 'tom-ford',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'Opulent, warm, and iconic London gentleman’s club atmosphere.',
                'desc': 'Tom Ford’s affection for London inspired this scent, reminiscent of an English gentleman’s club redolent with spice and rich tobacco leaf.',
                'top': 'Tobacco Leaf, Spicy Notes',
                'heart': 'Tonka Bean, Tobacco Blossom, Vanilla, Cacao',
                'base': 'Dry Fruit Accord, Rich Woods',
                'image': 'https://images.unsplash.com/photo-1508746829417-e6f548d8d6ed?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'TF-TV-10', Decimal('280.00'), 12, False),
                    ('50ml Eau de Parfum', 50, 'TF-TV-50', Decimal('1320.00'), 10, True),
                    ('100ml Eau de Parfum', 100, 'TF-TV-100', Decimal('1890.00'), 6, False),
                ]
            },
            # 12
            {
                'title': 'Oud Wood',
                'brand': 'tom-ford',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'Exotic rosewood, cardamom, and rare smoky agarwood.',
                'desc': 'One of the most rare, precious, and expensive ingredients in a perfumer’s arsenal, oud wood is often burned in incense-filled temples.',
                'top': 'Rosewood, Cardamom, Chinese Pepper',
                'heart': 'Oud Wood, Sandalwood, Vetiver',
                'base': 'Tonka Bean, Vanilla, Amber',
                'image': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('50ml Eau de Parfum', 50, 'TF-OW-50', Decimal('1320.00'), 8, True),
                    ('100ml Eau de Parfum', 100, 'TF-OW-100', Decimal('1890.00'), 5, False),
                ]
            },
            # 13
            {
                'title': 'Naxos',
                'brand': 'xerjoff',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'Celebrating Sicily with crisp citrus, sweet Mediterranean honey, and tobacco.',
                'desc': 'Naxos celebrates Sicily and its beauty, accented by top notes of bergamot, lemon, and lavender that lead to an inspiring heart of cinnamon, honey, and cashmeran.',
                'top': 'Bergamot, Lemon, Lavender',
                'heart': 'Sambac Jasmine, Cinnamon, Honey, Cashmeran',
                'base': 'Tobacco Leaf, Tonka Bean, Vanilla Berries',
                'image': 'https://images.unsplash.com/photo-1547887537-6158d64c35b3?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'XER-NAX-10', Decimal('220.00'), 15, False),
                    ('100ml Eau de Parfum', 100, 'XER-NAX-100', Decimal('1250.00'), 10, True),
                ]
            },
            # 14
            {
                'title': 'Erba Pura',
                'brand': 'xerjoff',
                'category': 'unisex',
                'family': 'fresh-citrus',
                'conc': Product.Concentration.EDP,
                'short': 'An intoxicating elixir of Mediterranean fruits and sensual white musk.',
                'desc': 'Erba Pura is a delicious and modern blend of Mediterranean citrus fruits layered over a warm, sensual amber and Madagascar vanilla base.',
                'top': 'Sicilian Orange, Sicilian Lemon, Calabrian Bergamot',
                'heart': 'Mediterranean Fruit Basket',
                'base': 'White Musk, Ambergris, Madagascar Vanilla',
                'image': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('100ml Eau de Parfum', 100, 'XER-EP-100', Decimal('1190.00'), 8, True),
                ]
            },
            # 15
            {
                'title': 'Gypsy Water',
                'brand': 'byredo',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'An ode to nomadic glamour: pine needle warmth, sandalwood, and citrus.',
                'desc': 'Gypsy Water is an awakening of romance and nature. The scent of fresh soil, deep pine forests, and campfires evokes the dream of a free, nomadic lifestyle.',
                'top': 'Bergamot, Lemon, Pepper, Juniper Berries',
                'heart': 'Incense, Pine Needles, Orris',
                'base': 'Amber, Vanilla, Sandalwood',
                'image': 'https://images.unsplash.com/photo-1588405748880-12d1d2a59f75?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('10ml Travel Discovery', 10, 'BYR-GW-10', Decimal('170.00'), 12, False),
                    ('50ml Eau de Parfum', 50, 'BYR-GW-50', Decimal('890.00'), 9, False),
                    ('100ml Eau de Parfum', 100, 'BYR-GW-100', Decimal('1290.00'), 11, True),
                ]
            },
            # 16
            {
                'title': 'Bal d’Afrique',
                'brand': 'byredo',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'Warm vetiver and vibrant Parisian avant-garde African celebration.',
                'desc': 'Bal d’Afrique is Ben Gorham’s love letter to Africa. A focus on celebration, reaching out to the vibrant culture and music of late 1920s Paris.',
                'top': 'African Marigold, Bergamot, Buchu, Lemon, Neroli',
                'heart': 'Cyclamen, Jasmine Petals, Violet',
                'base': 'Black Amber, Moroccan Cedarwood, Musk, Vetiver',
                'image': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('50ml Eau de Parfum', 50, 'BYR-BA-50', Decimal('890.00'), 10, False),
                    ('100ml Eau de Parfum', 100, 'BYR-BA-100', Decimal('1290.00'), 7, True),
                ]
            },
            # 17
            {
                'title': 'Portrait of a Lady',
                'brand': 'frederic-malle',
                'category': 'women',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': '400 Turkish roses per 100ml bottle, draped in patchouli and frankincense.',
                'desc': 'Considered one of modern perfumery’s crowning achievements by master perfumer Dominique Ropion. A symphonic rose layered with frankincense, cinnamon, and patchouli.',
                'top': 'Rose, Clove, Raspberry, Blackcurrant, Cinnamon',
                'heart': 'Patchouli, Incense, Sandalwood',
                'base': 'Musk, Amber, Benzoin',
                'image': 'https://images.unsplash.com/photo-1582211594533-268f4f1edcb9?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'FM-POAL-10', Decimal('290.00'), 10, False),
                    ('50ml Eau de Parfum', 50, 'FM-POAL-50', Decimal('1250.00'), 6, False),
                    ('100ml Eau de Parfum', 100, 'FM-POAL-100', Decimal('1850.00'), 8, True),
                ]
            },
            # 18
            {
                'title': 'Philosykos',
                'brand': 'diptyque',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'The Greek summer memory: raw green fig leaves, bark, and milky sap.',
                'desc': 'An ode to the whole fig tree: the green freshness of the leaves, the density of the white wood, the milky flavor of the ripe figs in Mount Pelion.',
                'top': 'Fig Leaf, Fig Fruit',
                'heart': 'Green Coconut Accord, Floral Accents',
                'base': 'Fig Tree Bark, Cedarwood',
                'image': 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('75ml Eau de Parfum', 75, 'DIP-PHIL-75', Decimal('890.00'), 12, True),
                ]
            },
            # 19
            {
                'title': 'Interlude Man',
                'brand': 'amouage',
                'category': 'men',
                'family': 'leather-smoke',
                'conc': Product.Concentration.EDP,
                'short': 'Known as the "Blue Beast": unbridled frankincense, myrrh, oregano, and leather.',
                'desc': 'Inspired by chaos and disorder, this spicy and woody fragrance masquerades an interlude moment of harmony in its heart with sacred frankincense and golden opoponax.',
                'top': 'Bergamot, Oregano, Pimento Berry Oil',
                'heart': 'Amber, Frankincense, Cistus, Opoponax',
                'base': 'Leather, Agarwood Smoke, Patchouli, Sandalwood',
                'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('100ml Eau de Parfum', 100, 'AMU-INT-100', Decimal('1590.00'), 6, True),
                ]
            },
            # 20
            {
                'title': 'Reflection Man',
                'brand': 'amouage',
                'category': 'men',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'Sublime refinement: aromatic rosemary, neroli, and creamy sandalwood.',
                'desc': 'Reflection Man embodies the spirit of refinement. Crisp floral notes of jasmine and orris are grounded by rich cedarwood and vetiver.',
                'top': 'Rosemary, Red Pepper Berries, Bitter Orange Leaves',
                'heart': 'Neroli, Orris, Jasmine, Ylang-Ylang',
                'base': 'Vetiver, Cedarwood, Sandalwood, Patchouli',
                'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('100ml Eau de Parfum', 100, 'AMU-REF-100', Decimal('1590.00'), 8, True),
                ]
            },
            # 21
            {
                'title': 'Hacivat',
                'brand': 'nishane',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EXTRAIT,
                'short': 'High-concentration citrus chypre with pineapple, clear cedar, and oakmoss.',
                'desc': 'A tribute to elegance, kindness, and art. Inspired by the traditional shadow play character, Hacivat delivers an unforgettable sillage of pineapple and clean woods.',
                'top': 'Bergamot, Pineapple, Grapefruit',
                'heart': 'Jasmine, Patchouli, Cedarwood',
                'base': 'Clearwood, Oakmoss, Dry Timberwood',
                'image': 'https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Extrait', 10, 'NSH-HAC-10', Decimal('220.00'), 15, False),
                    ('50ml Extrait de Parfum', 50, 'NSH-HAC-50', Decimal('980.00'), 10, True),
                    ('100ml Extrait de Parfum', 100, 'NSH-HAC-100', Decimal('1490.00'), 7, False),
                ]
            },
            # 22
            {
                'title': 'Ani',
                'brand': 'nishane',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EXTRAIT,
                'short': 'A romantic, warm vanilla masterpiece infused with spicy ginger and cardamom.',
                'desc': 'Ani is an ancient metropolis situated on a borderland. A fragrance created to tear down walls, featuring an opulent ginger and Madagascan vanilla heart.',
                'top': 'Ginger, Bergamot, Pink Pepper, Green Notes',
                'heart': 'Cardamom, Blackcurrant, Turkish Rose',
                'base': 'Vanilla, Benzoin, Sandalwood, Cedar, Patchouli, Ambergris',
                'image': 'https://images.unsplash.com/photo-1508746829417-e6f548d8d6ed?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('50ml Extrait de Parfum', 50, 'NSH-ANI-50', Decimal('980.00'), 9, True),
                    ('100ml Extrait de Parfum', 100, 'NSH-ANI-100', Decimal('1490.00'), 5, False),
                ]
            },
            # 23
            {
                'title': 'Gris Charnel',
                'brand': 'bdk',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'Sensual Parisian stroll: velvety black tea, purple fig, cardamom, and bourbon vetiver.',
                'desc': 'Silver moon over the Jardin du Luxembourg. Gris Charnel is an erotic, cozy skin scent centered around velvety fig, spiced cardamom, and pure sandalwood.',
                'top': 'Fig, Black Tea Pure Extract, Cardamom Essence',
                'heart': 'Iris Absolute, Bourbon Vetiver',
                'base': 'Sandalwood from India, Tonka Bean Absolute',
                'image': 'https://images.unsplash.com/photo-1547887537-6158d64c35b3?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'BDK-GC-10', Decimal('180.00'), 20, False),
                    ('100ml Eau de Parfum', 100, 'BDK-GC-100', Decimal('950.00'), 12, True),
                ]
            },
            # 24
            {
                'title': 'Rouge Smoking',
                'brand': 'bdk',
                'category': 'women',
                'family': 'gourmand',
                'conc': Product.Concentration.EDP,
                'short': 'Cherry liqueur, black vanilla, pink peppercorn, and white musk in Pigalle.',
                'desc': 'Inspired by the vibrant district of Pigalle. Rouge Smoking blends intoxicating cherry syrup with labdanum and sensual tonka bean.',
                'top': 'Bergamot, Cherry Accord, Pink Peppercorn',
                'heart': 'Black Vanilla, Heliotrope',
                'base': 'Ambroxan, Cashmeran, Tonka Bean, Labdanum, White Musk',
                'image': 'https://images.unsplash.com/photo-1582211594533-268f4f1edcb9?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('100ml Eau de Parfum', 100, 'BDK-RS-100', Decimal('950.00'), 8, True),
                ]
            },
            # 25
            {
                'title': 'Jazz Club',
                'brand': 'replica',
                'category': 'men',
                'family': 'leather-smoke',
                'conc': Product.Concentration.EDT,
                'short': 'Brooklyn 2013: heady cocktails, cured cigar smoke, and antique leather armchairs.',
                'desc': 'Jazz Club immortalizes the masculine and exhilarating ambiance of a Brooklyn jazz club. Notes of dark rum, tobacco leaf, and warm vanilla liqueur.',
                'top': 'Pink Pepper, Neroli, Lemon',
                'heart': 'Rum Absolute, Clary Sage, Java Vetiver',
                'base': 'Tobacco Leaf, Vanilla Bean, Styrax',
                'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Spray', 10, 'MM-JC-10', Decimal('150.00'), 25, False),
                    ('100ml Eau de Toilette', 100, 'MM-JC-100', Decimal('680.00'), 14, True),
                ]
            },
            # 26
            {
                'title': 'By the Fireplace',
                'brand': 'replica',
                'category': 'unisex',
                'family': 'woody',
                'conc': Product.Concentration.EDT,
                'short': 'Chamonix 1971: crackling chestnut embers and frost on the alpine window.',
                'desc': 'The cozy and comforting sensation of a crackling fire on a winter evening. Chestnuts roasting, sweet orange flower, and warming cashmeran.',
                'top': 'Pink Pepper, Orange Flower Petals, Clove Oil',
                'heart': 'Chestnut Accord, Gaïac Wood Oil, Cade Oil',
                'base': 'Vanilla Accord, Peru Balsam, Cashmeran',
                'image': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('10ml Travel Spray', 10, 'MM-BTF-10', Decimal('150.00'), 18, False),
                    ('100ml Eau de Toilette', 100, 'MM-BTF-100', Decimal('680.00'), 11, True),
                ]
            },
            # 27
            {
                'title': 'Halfeti',
                'brand': 'penhaligons',
                'category': 'unisex',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'Mysterious black roses blooming along the banks of the Euphrates river.',
                'desc': 'An intoxicating, mysterious fragrance of vigorous grapefruit, Levantine spice and black rose drenched in dark oud, patchouli and leather.',
                'top': 'Grapefruit, Bergamot, Green Notes, Armoise, Cypress',
                'heart': 'Cumin, Nutmeg, Violet, Saffron, Rose, Jasmine, Lily of the Valley',
                'base': 'Leather, Oud, Amber, Resins, Tonka, Vanilla, Sandalwood',
                'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('10ml Travel Discovery', 10, 'PEN-HALF-10', Decimal('230.00'), 15, False),
                    ('100ml Eau de Parfum', 100, 'PEN-HALF-100', Decimal('1290.00'), 9, True),
                ]
            },
            # 28
            {
                'title': 'The Tragedy of Lord George',
                'brand': 'penhaligons',
                'category': 'men',
                'family': 'oriental-amber',
                'conc': Product.Concentration.EDP,
                'short': 'Aristocratic British honor: shaving soap, velvety tonka, and aged rum.',
                'desc': 'Lord George is a wealthy and respected man, the quintessential patriarch. He seems to embody the noblest values of the aristocracy: virtue, respect, and loyalty.',
                'top': 'Brandy, Shaving Soap Accord',
                'heart': 'Tonka Bean, Lavender',
                'base': 'Golden Amber, Cedarwood',
                'image': 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('75ml Eau de Parfum', 75, 'PEN-LORD-75', Decimal('1350.00'), 6, True),
                ]
            },
            # 29 (Gift Set)
            {
                'title': 'Maison Francis Kurkdjian Wardrobe for Her',
                'brand': 'mfk',
                'category': 'gift-sets',
                'family': 'floral',
                'conc': Product.Concentration.EDP,
                'short': 'Luxury coffret of 8 x 11ml iconic feminine fragrances including Baccarat Rouge & À la Rose.',
                'desc': 'The Fragrance Wardrobe for Her is a fine selection of eight 11ml perfume refills, representing an exceptional olfactory wardrobe designed for every mood and season.',
                'top': 'Assorted French Haute Parfumerie Openings',
                'heart': 'May Rose, Damascena, Egyptian Jasmine Grandiflorum',
                'base': 'Precious Woods, Ambergris, Bourbon Vanilla',
                'image': 'https://images.unsplash.com/photo-1547887537-6158d64c35b3?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('Luxury Gift Coffret (8 x 11ml)', 88, 'MFK-SET-HER', Decimal('1050.00'), 8, True),
                ]
            },
            # 30 (Gift Set)
            {
                'title': 'Creed Men’s Royal Discovery Coffret',
                'brand': 'creed',
                'category': 'gift-sets',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'Exclusive coffret featuring Aventus, Green Irish Tweed, and Silver Mountain Water (3 x 10ml).',
                'desc': 'A magnificent gift set containing three of the House of Creed’s most legendary masculine masterworks in 10ml travel atomizers, presented in a gold-embossed bespoke coffret.',
                'top': 'Lemon, Pineapple, Bergamot, Peppermint',
                'heart': 'Patchouli, Iris, Jasmine, Green Tea',
                'base': 'Oakmoss, Birch, Ambergris, Sandalwood',
                'image': 'https://images.unsplash.com/photo-1523293182086-7651a899d37f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('Royal Discovery Coffret (3 x 10ml)', 30, 'CRD-SET-MEN', Decimal('750.00'), 12, True),
                ]
            },
            # 31 (Gift Set)
            {
                'title': 'Kilian Paris The Liquors Discovery Miniature Set',
                'brand': 'kilian',
                'category': 'gift-sets',
                'family': 'gourmand',
                'conc': Product.Concentration.EDP,
                'short': 'Four 7.5ml carafes of Angels’ Share, Roses on Ice, Apple Brandy, and Blue Moon.',
                'desc': 'Explore Kilian Hennessy’s speakeasy heritage with four miniature crystal carafes, paying homage to legendary cocktails, aged cognacs, and botanical gin.',
                'top': 'Cognac Oil, Gin Botanicals, Green Apple Crisp',
                'heart': 'Cinnamon Bark, Rose, Oak Absolute',
                'base': 'Praline, Vanilla, Cedarwood',
                'image': 'https://images.unsplash.com/photo-1595425970377-c9703cf48b6d?auto=format&fit=crop&w=800&q=80',
                'featured': False,
                'variants': [
                    ('Liquors Miniature Set (4 x 7.5ml)', 30, 'KLN-SET-LIQ', Decimal('890.00'), 10, True),
                ]
            },
            # 32 (Gift Set)
            {
                'title': 'Le Labo Classic Discovery Set',
                'brand': 'le-labo',
                'category': 'gift-sets',
                'family': 'woody',
                'conc': Product.Concentration.EDP,
                'short': 'Five 5ml sprays of Santal 33, Thé Noir 29, Rose 31, Another 13, and Bergamote 22.',
                'desc': 'Created to discover five of Le Labo’s most cherished fine fragrances in an authentic kraft cardboard box sealed with personalized label.',
                'top': 'Violet, Bergamot, Cumin, Pear, Citrus',
                'heart': 'Cardamom, Rose, Fig, Iris, Jasmine',
                'base': 'Australian Sandalwood, Vetiver, Ambrox 9, Musk',
                'image': 'https://images.unsplash.com/photo-1594035910387-fea47794261f?auto=format&fit=crop&w=800&q=80',
                'featured': True,
                'variants': [
                    ('Discovery Set (5 x 5ml)', 25, 'LL-SET-5', Decimal('620.00'), 15, True),
                ]
            },
        ]

        # Map of authentic perfume bottle image URLs
        IMG_URLS = {
            'Baccarat Rouge 540': 'https://fimgs.net/mdimg/perfume/375x500.39359.jpg',
            'Grand Soir': 'https://fimgs.net/mdimg/perfume/375x500.41054.jpg',
            'Aventus': 'https://fimgs.net/mdimg/perfume/375x500.9828.jpg',
            'Silver Mountain Water': 'https://fimgs.net/mdimg/perfume/375x500.470.jpg',
            'Santal 33': 'https://fimgs.net/mdimg/perfume/375x500.12201.jpg',
            'Thé Noir 29': 'https://fimgs.net/mdimg/perfume/375x500.31858.jpg',
            'Angels’ Share': 'https://fimgs.net/mdimg/perfume/375x500.62615.jpg',
            'Black Phantom "Memento Mori"': 'https://fimgs.net/mdimg/perfume/375x500.43632.jpg',
            'Delina': 'https://fimgs.net/mdimg/perfume/375x500.43864.jpg',
            'Herod': 'https://fimgs.net/mdimg/perfume/375x500.16939.jpg',
            'Tobacco Vanille': 'https://fimgs.net/mdimg/perfume/375x500.1825.jpg',
            'Oud Wood': 'https://fimgs.net/mdimg/perfume/375x500.1826.jpg',
            'Naxos': 'https://fimgs.net/mdimg/perfume/375x500.30529.jpg',
            'Erba Pura': 'https://fimgs.net/mdimg/perfume/375x500.55157.jpg',
            'Gypsy Water': 'https://fimgs.net/mdimg/perfume/375x500.3575.jpg',
            'Bal d’Afrique': 'https://fimgs.net/mdimg/perfume/375x500.6458.jpg',
            'Portrait of a Lady': 'https://fimgs.net/mdimg/perfume/375x500.10211.jpg',
            'Philosykos': 'https://fimgs.net/mdimg/perfume/375x500.3865.jpg',
            'Interlude Man': 'https://fimgs.net/mdimg/perfume/375x500.15294.jpg',
            'Reflection Man': 'https://fimgs.net/mdimg/perfume/375x500.924.jpg',
            'Hacivat': 'https://fimgs.net/mdimg/perfume/375x500.44174.jpg',
            'Ani': 'https://fimgs.net/mdimg/perfume/375x500.54785.jpg',
            'Gris Charnel': 'https://fimgs.net/mdimg/perfume/375x500.57016.jpg',
            'Rouge Smoking': 'https://fimgs.net/mdimg/perfume/375x500.51495.jpg',
            'Jazz Club': 'https://fimgs.net/mdimg/perfume/375x500.20541.jpg',
            'By the Fireplace': 'https://fimgs.net/mdimg/perfume/375x500.31623.jpg',
            'Halfeti': 'https://fimgs.net/mdimg/perfume/375x500.31396.jpg',
            'The Tragedy of Lord George': 'https://fimgs.net/mdimg/perfume/375x500.40606.jpg',
            'Maison Francis Kurkdjian Wardrobe for Her': 'https://fimgs.net/mdimg/perfume/375x500.39359.jpg',
            'Creed Men’s Royal Discovery Coffret': 'https://fimgs.net/mdimg/perfume/375x500.9828.jpg',
            'Kilian Paris The Liquors Discovery Miniature Set': 'https://fimgs.net/mdimg/perfume/375x500.62615.jpg',
            'Le Labo Classic Discovery Set': 'https://fimgs.net/mdimg/perfume/375x500.12201.jpg',
        }

        # Populate products and variants
        created_count = 0
        for item in catalog:
            brand_obj = brands[item['brand']]
            cat_obj = categories[item['category']]
            fam_obj = families[item['family']]
            image_link = IMG_URLS.get(item['title'], item['image'])

            prod, created = Product.objects.get_or_create(
                title=item['title'],
                brand=brand_obj,
                defaults={
                    'category': cat_obj,
                    'fragrance_family': fam_obj,
                    'concentration': item['conc'],
                    'short_description': item['short'],
                    'description': item['desc'],
                    'top_notes': item['top'],
                    'heart_notes': item['heart'],
                    'base_notes': item['base'],
                    'image_url': image_link,
                    'is_featured': item['featured'],
                    'is_active': True,
                }
            )
            if not created:
                prod.image_url = image_link
                prod.save(update_fields=['image_url'])

            if created:
                created_count += 1
                for label, size_ml, sku, price, stock, is_default in item['variants']:
                    ProductVariant.objects.create(
                        product=prod,
                        size_label=label,
                        size_ml=size_ml,
                        sku=sku,
                        price=price,
                        stock_quantity=stock,
                        is_default=is_default,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"==> Database Seed Complete! {Product.objects.count()} Curated Fragrances, "
            f"{ProductVariant.objects.count()} Size Variants across 4 Categories."
        ))

