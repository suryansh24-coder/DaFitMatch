import bs4
import subprocess
import tempfile
import sys

with open('index.html', 'r') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

for i, script in enumerate(scripts):
    if script.string:
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as tf:
            tf.write(script.string)
            tf.flush()
            result = subprocess.run(['node', '--check', tf.name], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error in script block {i}")
                print(result.stderr.splitlines()[0:3])
                
                # Try to extract the exact line of the syntax error
                for line in result.stderr.splitlines():
                    if tf.name in line:
                        try:
                            line_num = int(line.split(':')[1])
                            print(f"Line {line_num}:")
                            lines = script.string.splitlines()
                            for j in range(max(0, line_num-5), min(len(lines), line_num+5)):
                                prefix = ">> " if j == line_num - 1 else "   "
                                print(f"{prefix}{j+1}: {lines[j]}")
                        except:
                            pass
