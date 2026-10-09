const fs = require('fs');

const configJs = fs.readFileSync('config.js', 'utf8');
const match = configJs.match(/GOOGLE_CLIENT_ID:\s*['"]([^'"]+)['"]/);
const clientId = match ? match[1] : null;

console.log('--- DIAGNOSTIC ---');
console.log('Exists:', !!clientId);
if (clientId) {
    console.log('First 8:', clientId.substring(0, 8));
    console.log('Last 20:', clientId.substring(clientId.length - 20));
}
console.log('Origin: http://localhost:8082'); // This is the server origin
console.log('------------------');
