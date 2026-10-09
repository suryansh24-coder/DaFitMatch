import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace image source
html = html.replace('src="couple-hero.png"', 'src="hero-wide.png"')

# Replace aspect ratio classes
old_aspect = 'aspect-[4/3] sm:aspect-video lg:aspect-[9/5]'
new_aspect = 'aspect-video sm:aspect-[3/1] lg:aspect-[4/1]'
html = html.replace(old_aspect, new_aspect)

with open('index.html', 'w') as f:
    f.write(html)

print("Image and aspect ratio updated!")
