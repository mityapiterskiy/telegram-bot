from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('TOKEN')

# Create Flask app
app = Flask(__name__)

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

@app.route('/', methods=['GET'])
def home():
    token_status = "SET" if BOT_TOKEN else "NOT SET"
    return jsonify({
        "status": "Bot is running!", 
        "token_status": token_status,
        "token_length": len(BOT_TOKEN) if BOT_TOKEN else 0
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram."""
    return jsonify({"status": "ok", "message": "Webhook received"})

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Set webhook URL for the bot."""
    webhook_url = request.args.get('url')
    if webhook_url:
        result = application.bot.set_webhook(url=webhook_url)
        return jsonify({"webhook_set": result})
    return jsonify({"error": "No URL provided"})

if __name__ == '__main__':
    # For local development, use polling
    application.run_polling(allowed_updates=Update.ALL_TYPES) 