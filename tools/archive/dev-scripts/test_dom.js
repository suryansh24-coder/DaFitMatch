const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });
const window = dom.window;
const document = window.document;

console.log("typeof openCataloguePanel:", typeof window.openCataloguePanel);
console.log("typeof closeCataloguePanel:", typeof window.closeCataloguePanel);

if (typeof window.openCataloguePanel === 'function') {
    console.log("[DaFitMatch Catalogue] OPEN CLICKED");
    window.openCataloguePanel();
    
    const drawer = document.getElementById('catalogue-drawer');
    console.log("Drawer details:", {
        exists: !!drawer,
        className: drawer?.className,
    });
} else {
    console.log("ERROR: openCataloguePanel is not a function in the DOM.");
}
