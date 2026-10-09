with open('index.html', 'r') as f:
    html = f.read()

html = html.replace("selectOutfit(\\'${outfit.id}\\')", "selectOutfit('${outfit.id}')")

with open('index.html', 'w') as f:
    f.write(html)
print("Quotes fixed.")
