import http.server
import socketserver
from urllib.parse import unquote
import mimetypes
import os
import webbrowser  # Import webbrowser module

# Add custom MIME types for Unity WebGL files
mimetypes.add_type('application/octet-stream', '.unityweb')
mimetypes.add_type('application/wasm', '.wasm')

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        path = unquote(self.path)
        if path.endswith('.gz'):
            self.send_header('Content-Encoding', 'gzip')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS for local testing
        super().end_headers()

    def guess_type(self, path):
        # Override to handle .gz files correctly
        base, ext = os.path.splitext(path)
        if ext == '.gz':
            base, inner_ext = os.path.splitext(base)
            return mimetypes.guess_type(base + inner_ext)[0] or 'application/octet-stream'
        return super().guess_type(path)

Handler = CustomHandler

# Start the server and open the browser
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving at port {PORT}, opening browser to {url}")
    
    # Open the default web browser to localhost:8000
    webbrowser.open(url)
    
    # Start the server
    httpd.serve_forever()