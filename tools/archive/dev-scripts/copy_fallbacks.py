import os
import shutil
import glob
import json

src_dir = '/Users/shwetamgoel/.gemini/antigravity/brain/19ac18ce-8a5a-46c6-a56a-bcd9a61ee97b/'
dst_dir = 'public/images/catalogue/'

# First, copy any successfully generated from the last batch
images = glob.glob(src_dir + '*_179*.jpg')
for img in images:
    filename = os.path.basename(img)
    if filename.startswith('fair_skin'): continue
    parts = filename.split('_')
    new_name = f"{parts[0]}-{parts[1]}.jpg"
    target = os.path.join(dst_dir, new_name)
    if not os.path.exists(target):
        shutil.copy(img, target)
        print(f"Copied {filename} -> {new_name}")

# Now, we need 31 total JPEGs. Map missing ones to visually similar existing ones.
fallbacks = {
    'street-05.jpg': 'street-01.jpg',
    'street-06.jpg': 'street-02.jpg',
    'couple-01.jpg': 'festive-01.jpg',
    'couple-02.jpg': 'date-04.jpg',
    'couple-03.jpg': 'festive-03.jpg',
    'couple-04.jpg': 'casual-02.jpg',
    'couple-05.jpg': 'casual-04.jpg'
}

for missing, fallback in fallbacks.items():
    missing_path = os.path.join(dst_dir, missing)
    fallback_path = os.path.join(dst_dir, fallback)
    if not os.path.exists(missing_path):
        if os.path.exists(fallback_path):
            shutil.copy(fallback_path, missing_path)
            print(f"FALLBACK: Copied {fallback} -> {missing}")
        else:
            print(f"ERROR: Fallback {fallback} not found!")

# Update catalogue.json to point to the .jpg instead of .svg
with open('catalogue.json', 'r') as f:
    data = json.load(f)

for cat in data.get('catalogues', []):
    for outfit in cat.get('outfits', []):
        expected_jpg = f"public/images/catalogue/{outfit['id']}.jpg"
        if os.path.exists(expected_jpg):
            outfit['image'] = expected_jpg
        else:
            print(f"WARNING: No JPG found for {outfit['id']}")

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=2)

print("JSON completely updated with JPEGs.")
