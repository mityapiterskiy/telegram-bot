import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('TOKEN')

def handler(request):
    """Vercel function handler."""
    # Get request data
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    body = request.get('body', '')
    
    # Parse JSON body if present
    try:
        data = json.loads(body) if body else {}
    except:
        data = {}
    
    # Handle different routes
    if path == '/' and method == 'GET':
        token_status = "SET" if BOT_TOKEN else "NOT SET"
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                "status": "Bot is running!", 
                "token_status": token_status,
                "token_length": len(BOT_TOKEN) if BOT_TOKEN else 0
            })
        }
    
    elif path == '/webhook' and method == 'POST':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"status": "ok", "message": "Webhook received"})
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Not found"})
        } 