import json

with open('catalogue.json', 'r') as f:
    data = json.load(f)

for category in data.get('catalogues', []):
    for outfit in category.get('outfits', []):
        if outfit.get('id') == 'casual-01':
            if 'tryOnVideo' in outfit:
                del outfit['tryOnVideo']
            # We can also clean up the others if they have fake MP4 paths to avoid more 404s, but user explicitly said:
            # "For casual-01, change: tryOnVideo: ... to tryOnVideo: '' or remove"
            # Actually, let's remove it for all outfits that have a tryOnVideo that starts with /videos/ to be completely safe from 404s,
            # wait, the user said "We do NOT have try-on MP4 files right now. For the demo, make TRY-ON IMAGE the primary path. In the catalogue data, remove/ignore nonexistent tryOnVideo values when the file does not exist."
            # So I will delete ALL tryOnVideo keys from the catalogue.

for category in data.get('catalogues', []):
    for outfit in category.get('outfits', []):
        if 'tryOnVideo' in outfit:
            del outfit['tryOnVideo']

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=4)
