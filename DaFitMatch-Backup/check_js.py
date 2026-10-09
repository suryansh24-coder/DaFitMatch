import bs4
import subprocess
import tempfile
import sys

with open('index.html', 'r') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

has_error = False
for i, script in enumerate(scripts):
    if script.string:
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tf:
            tf.write(script.string)
            tf.flush()
            result = subprocess.run(['node', '--check', tf.name], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error in script block {i}:\n")
                # Remove the temp file path from the output for clarity
                error_lines = result.stderr.splitlines()
                for line in error_lines:
                    if tf.name not in line:
                        print(line)
                print("-------------")
                print("Code snippet:")
                lines = script.string.splitlines()
                # Print the line numbers
                for idx, l in enumerate(lines):
                    print(f"{idx+1}: {l}")
                print("=============\n")
                has_error = True

if not has_error:
    print("All script blocks passed Node.js syntax check.")
