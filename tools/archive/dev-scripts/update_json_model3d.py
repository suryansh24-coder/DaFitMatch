import json

with open('catalogue.json', 'r') as f:
    data = json.load(f)

for cat in data.get('catalogues', []):
    for outfit in cat.get('outfits', []):
        outfit['model3D'] = f"/models/outfits/{outfit['id']}.glb"
        
        # Also ensure Couple outfits have person1/person2 model3D paths if needed
        if outfit.get('gender') == 'couple':
            if 'person1' in outfit:
                outfit['person1']['model3D'] = f"/models/outfits/{outfit['id']}-person1.glb"
            if 'person2' in outfit:
                outfit['person2']['model3D'] = f"/models/outfits/{outfit['id']}-person2.glb"

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Updated catalogue.json with model3D fields.")
