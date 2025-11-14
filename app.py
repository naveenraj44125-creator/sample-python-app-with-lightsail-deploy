#!/usr/bin/env python3
# sample-python-app-with-lightsail-deploy
# Deployed using Reusable GitHub Actions Workflow

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>sample-python-app-with-lightsail-deploy</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }}
        h1 {{ color: #667eea; margin-bottom: 20px; }}
        .badge {{
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            margin: 10px 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 sample-python-app-with-lightsail-deploy</h1>
        <p>Deployed using Reusable GitHub Actions Workflow</p>
        <div class="badge">✅ Python 3</div>
        <div class="badge">☁️ AWS Lightsail</div>
        <div class="badge">🔄 Automated Deployment</div>
    </div>
</body>
</html>'''
            self.wfile.write(html.encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(health).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def log_message(self, format, *args):
        print(f"{datetime.now().isoformat()} - {format % args}")

if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('', PORT), AppHandler)
    print(f'🚀 sample-python-app-with-lightsail-deploy running on port {PORT}')
    print(f'📍 Visit: http://localhost:{PORT}')
    server.serve_forever()
