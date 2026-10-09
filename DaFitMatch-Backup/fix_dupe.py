import re

with open('index.html', 'r') as f:
    html = f.read()

# Find the catalogue script block
script_start = html.find('<script>\nwindow.dafitmatchState')
if script_start != -1:
    script_end = html.find('</script>', script_start) + 9
    first_block = html[script_start:script_end]
    
    # Check if there is another one
    second_start = html.find('<script>\nwindow.dafitmatchState', script_end)
    if second_start != -1:
        second_end = html.find('</script>', second_start) + 9
        html = html[:second_start] + html[second_end:]
        with open('index.html', 'w') as f:
            f.write(html)
        print("Duplicate catalogue script removed!")
    else:
        print("No duplicate found.")
