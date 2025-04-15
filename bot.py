from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram import Update
import os
from dotenv import load_dotenv

# Import custom handlers
from handlers.start import start_handler
from handlers.feedback import feedback_handler
from handlers.mood import mood_handler
from handlers.chat_handler import generate_empathetic_response

load_dotenv()

# Declare global app variable
app = None

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_handler(update, context)

# Feedback command
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await feedback_handler(update, context)

# Mood checker (daily or keyword based)
async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mood_handler(update, context)

# Default message → AI mental health support
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = await generate_empathetic_response(user_input)
    await update.message.reply_text(response)

# Setup the Telegram bot app
async def setup_bot():
    global app
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feedback", feedback))
    app.add_handler(CommandHandler("daily", handle_mood))

    # Text handler for normal messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

def get_app():
    return app
