import re

with open('index.html', 'r') as f:
    html = f.read()

test_script = """
<script>
console.log(
    '[DaFitMatch DEMO] RUNTIME selectOutfit =',
    typeof window.selectOutfit
);

window.selectOutfit = window.selectOutfit || function(outfitId) {
    console.error(
        '[DaFitMatch DEMO] selectOutfit fallback invoked:',
        outfitId
    );
};

console.log(
    '[DaFitMatch DEMO] FINAL selectOutFit =',
    typeof window.selectOutfit
);
</script>
"""

html = html.replace("</body>", test_script + "\n</body>")

with open('index.html', 'w') as f:
    f.write(html)
