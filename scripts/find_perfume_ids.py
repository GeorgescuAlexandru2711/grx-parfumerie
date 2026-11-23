import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

queries = [
    ('Baccarat Rouge 540', 'Baccarat Rouge 540'),
    ('Reflection Man', 'Reflection Man Amouage'),
    ('Grand Soir', 'Grand Soir MFK'),
    ('Aventus', 'Creed Aventus'),
    ('Silver Mountain Water', 'Silver Mountain Water Creed'),
    ('Santal 33', 'Santal 33 Le Labo'),
    ('Angels Share', 'Angels Share Kilian'),
    ('Black Phantom', 'Black Phantom Kilian'),
    ('Delina', 'Delina Parfums de Marly'),
    ('Herod', 'Herod Parfums de Marly'),
    ('Tobacco Vanille', 'Tobacco Vanille Tom Ford'),
    ('Oud Wood', 'Oud Wood Tom Ford'),
    ('Naxos', 'Naxos Xerjoff'),
    ('Erba Pura', 'Erba Pura Xerjoff'),
    ('Gypsy Water', 'Gypsy Water Byredo'),
    ('Bal d Afrique', 'Bal d Afrique Byredo'),
    ('Portrait of a Lady', 'Portrait of a Lady Frederic Malle'),
    ('Philosykos', 'Philosykos Diptyque'),
    ('Interlude Man', 'Interlude Man Amouage'),
    ('Hacivat', 'Hacivat Nishane'),
    ('Ani', 'Ani Nishane'),
    ('Gris Charnel', 'Gris Charnel BDK'),
    ('Rouge Smoking', 'Rouge Smoking BDK'),
    ('Jazz Club', 'Jazz Club Maison Margiela'),
    ('By the Fireplace', 'By the Fireplace Maison Margiela'),
    ('Halfeti', 'Halfeti Penhaligons'),
    ('Lord George', 'The Tragedy of Lord George Penhaligons'),
]

for label, q in queries:
    try:
        url = f"https://www.fragrantica.com/search/?query={q.replace(' ', '+')}"
        res = requests.get(url, headers=headers, timeout=8)
        # Find perfume links: /perfume/Brand/Name-12345.html
        links = re.findall(r'/perfume/[^"]+-(\d+)\.html', res.text)
        if links:
            perfume_id = links[0]
            img_url = f"https://fimgs.net/mdimg/perfume/375x500.{perfume_id}.jpg"
            print(f"{label} -> ID: {perfume_id} -> {img_url}")
        else:
            print(f"{label} -> NOT FOUND")
    except Exception as e:
        print(f"{label} -> ERROR: {e}")

