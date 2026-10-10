const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });
const window = dom.window;

console.log("typeof openCataloguePanel:", typeof window.openCataloguePanel);
if(typeof window.openCataloguePanel === 'function') {
    window.openCataloguePanel();
    const drawer = window.document.getElementById('catalogue-drawer');
    console.log("classes after open:", drawer.className);
}
