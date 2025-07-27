from http.server import BaseHTTPRequestHandler
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('TOKEN')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            token_status = "SET" if BOT_TOKEN else "NOT SET"
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "Bot is running!", 
                "token_status": token_status,
                "token_length": len(BOT_TOKEN) if BOT_TOKEN else 0
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        if self.path == '/webhook':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "ok", "message": "Webhook received"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode()) 