import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the Fashion Visual Frame div to be full width with an aspect ratio
old_frame = r'<div class="relative rounded-3xl overflow-hidden shadow-2xl border-4 border-white/50 group bg-slate-900/10">'
new_frame = '<div class="relative w-full aspect-[4/3] sm:aspect-video lg:aspect-[21/9] rounded-3xl overflow-hidden shadow-2xl border-4 border-white/50 group bg-slate-900/10">'

if old_frame in html:
    html = html.replace(old_frame, new_frame)
else:
    print("Could not find the frame div!")

# 2. Update the img tag to fill the aspect-ratio container
old_img = r'class="w-full max-h-\[580px\] sm:max-h-\[640px\] object-cover object-center transform scale-100 group-hover:scale-105 transition-transform duration-700 ease-out"'
new_img = 'class="absolute inset-0 w-full h-full object-cover object-center transform scale-100 group-hover:scale-105 transition-transform duration-700 ease-out"'

if old_img in html:
    html = html.replace(old_img, new_img)
else:
    print("Could not find the img classes!")

with open('index.html', 'w') as f:
    f.write(html)

print("Hero aspect ratio fixed!")
