import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from handlers.start import start_handler
from handlers.feedback import feedback_handler
from handlers.mood import handle_mood
from handlers.ai import ai_response_handler

app = None  # Global app instance

async def setup_bot():
    global app
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Use your env var here
    app = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("feedback", feedback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))

    await app.initialize()  # ✅ IMPORTANT: This fixes the runtime error!

    print("✅ Telegram bot initialized")

def get_app():
    return app

# Route message logic: decide which handler to call
async def route_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    # Custom logic to detect mood/intent
    mood_keywords = ["i dey", "i no", "i feel", "i wan yarn", "i dey stress"]
    if any(phrase in user_text for phrase in mood_keywords):
        await handle_mood(update, context)
    else:
        await ai_response_handler(update, context)
