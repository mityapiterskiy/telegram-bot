from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('TOKEN')

# Create the Application
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am your Telegram bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text('This is a help message.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

def handler(request):
    """Vercel function handler."""
    import asyncio
    
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
    
    elif path == '/set-webhook' and method == 'GET':
        # Extract URL from query parameters
        query = request.get('query', {})
        webhook_url = query.get('url', '')
        
        if webhook_url:
            result = application.bot.set_webhook(url=webhook_url)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"webhook_set": result})
            }
        else:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "No URL provided"})
            }
    
    else:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Not found"})
        }

if __name__ == '__main__':
    # For local development, use polling
    application.run_polling(allowed_updates=Update.ALL_TYPES) 