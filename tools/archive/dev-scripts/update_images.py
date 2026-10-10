import glob
import os
import shutil
import json

src_dir = '/Users/shwetamgoel/.gemini/antigravity/brain/19ac18ce-8a5a-46c6-a56a-bcd9a61ee97b/'
dst_dir = 'public/images/catalogue/'

# Find all recently generated jpegs (exclude fair_skin_model)
images = glob.glob(src_dir + '*_179*.jpg')

# Copy to correct names
for img in images:
    filename = os.path.basename(img)
    if filename.startswith('fair_skin'):
        continue
    # e.g. casual_01_1790953242025.jpg -> casual-01.jpg
    parts = filename.split('_')
    new_name = f"{parts[0]}-{parts[1]}.jpg"
    shutil.copy(img, os.path.join(dst_dir, new_name))
    print(f"Copied {filename} -> {new_name}")

# Update catalogue.json for existing jpegs
with open('catalogue.json', 'r') as f:
    data = json.load(f)

for cat in data.get('catalogues', []):
    for outfit in cat.get('outfits', []):
        expected_jpg = f"public/images/catalogue/{outfit['id']}.jpg"
        if os.path.exists(expected_jpg):
            outfit['image'] = expected_jpg

with open('catalogue.json', 'w') as f:
    json.dump(data, f, indent=2)

print("JSON updated with JPEGs.")
