import re

with open('index.html', 'r') as f:
    html = f.read()

# Increase vertical margin on the container
html = html.replace('relative w-full max-w-4xl my-2 flex', 'relative w-full max-w-4xl mt-12 mb-16 sm:mt-16 sm:mb-20 flex')

# 1. Style Match (Top Left)
old_style = 'absolute -top-4 -left-4 sm:top-10 sm:-left-10'
new_style = 'absolute -top-8 -left-2 sm:-top-12 sm:-left-12'
html = html.replace(old_style, new_style)

# 2. Occasion Badge (Top Right)
old_occasion = 'absolute -top-4 -right-4 sm:top-14 sm:-right-8'
new_occasion = 'absolute -top-6 -right-2 sm:-top-8 sm:-right-10'
html = html.replace(old_occasion, new_occasion)

# 3. Harmony Badge (Bottom Left)
old_harmony = 'absolute bottom-6 -left-6 sm:bottom-16 sm:-left-12'
new_harmony = 'absolute -bottom-8 -left-2 sm:-bottom-12 sm:-left-12'
html = html.replace(old_harmony, new_harmony)

# 4. Tryon Status (Bottom Right)
old_tryon = 'absolute bottom-8 -right-6 sm:bottom-12 sm:-right-8'
new_tryon = 'absolute -bottom-6 -right-2 sm:-bottom-10 sm:-right-10'
html = html.replace(old_tryon, new_tryon)

with open('index.html', 'w') as f:
    f.write(html)

print("Badges repositioned!")
