const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/index.html') {
        fs.readFile(path.join(__dirname, 'index.html'), (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Not found');
                return;
            }
            
            // Inject backend URL into the HTML
            const html = data.toString().replace(
                'window.backendURL || \'\'',
                'window.backendURL || \'http://localhost:8000\''
            );
            
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(html);
        });
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(3000, () => {
    console.log('Frontend development server running at http://localhost:3000');
    console.log('Backend should be running at http://localhost:8000');
});