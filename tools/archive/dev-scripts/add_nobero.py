import json

with open('catalogue.json', 'r') as f:
    data = json.load(f)

# Find streetwear catalogue
streetwear_cat = next(cat for cat in data['catalogues'] if cat['id'] == 'streetwear')

new_outfit = {
    "id": "street-06",
    "name": "NOBERO Oversized Co-ord",
    "gender": "men",
    "items": [
        "Oversized T-Shirt",
        "Matching Relaxed Shorts/Pants"
    ],
    "colors": ["Neutral"],
    "style": "Oversized Urban",
    "price": 1499,
    "platform": "Myntra",
    "matchScore": 95,
    "image": "",
    "productUrl": ""
}

streetwear_cat['outfits'].append(new_outfit)

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Added NOBERO to catalogue.json!")
