import json

with open('catalogue.json', 'r') as f:
    data = json.load(f)

for category in data.get('catalogues', []):
    for outfit in category.get('outfits', []):
        if 'person1' in outfit and 'tryOnVideo' in outfit['person1']:
            del outfit['person1']['tryOnVideo']
        if 'person2' in outfit and 'tryOnVideo' in outfit['person2']:
            del outfit['person2']['tryOnVideo']
        
        # Also let's double check if there are any other 'tryOnVideo'
        if 'tryOnVideo' in outfit:
            del outfit['tryOnVideo']

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=4)
