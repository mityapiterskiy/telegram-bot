from http.server import BaseHTTPRequestHandler
import json
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

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
        elif self.path == '/poll':
            # Poll for updates
            try:
                updates = asyncio.run(application.bot.get_updates())
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"updates": len(updates)}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        # Simple response for any POST request
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"status": "ok"}
        self.wfile.write(json.dumps(response).encode()) 