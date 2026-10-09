import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'function initCalibrationUI\(\) \{'
replacement = 'function initCalibrationUI() {\n    return; // DEMO: Remove calibration UI from screen\n'

html = re.sub(target, replacement, html)

with open('index.html', 'w') as f:
    f.write(html)
