import json

with open('catalogue.json', 'r') as f:
    data = json.load(f)

for cat in data.get('catalogues', []):
    for outfit in cat.get('outfits', []):
        cat_id = cat['id'] # e.g. casual
        outfit_id = outfit['id'] # e.g. casual-01
        
        outfit['tryOnImage'] = f"/images/try-on/{cat_id}/{outfit_id}.jpg"
        outfit['tryOnVideo'] = f"/videos/try-on/{cat_id}/{outfit_id}.mp4"
        
        if outfit.get('gender') == 'couple':
            if 'person1' in outfit:
                outfit['person1']['tryOnImage'] = f"/images/try-on/{cat_id}/{outfit_id}-person1.jpg"
                outfit['person1']['tryOnVideo'] = f"/videos/try-on/{cat_id}/{outfit_id}-person1.mp4"
            if 'person2' in outfit:
                outfit['person2']['tryOnImage'] = f"/images/try-on/{cat_id}/{outfit_id}-person2.jpg"
                outfit['person2']['tryOnVideo'] = f"/videos/try-on/{cat_id}/{outfit_id}-person2.mp4"

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Added tryOnImage and tryOnVideo fields to catalogue.json.")
