import os
from telegram.ext import ApplicationBuilder
from handlers.start import start_handler
from handlers.feedback import feedback_handler
from handlers.mood import mood_handler
from handlers.intent import intent_handler
from handlers.daily import daily_handler

# Global app object
app = None

async def setup_bot():
    global app

    # Initialize the bot with your Telegram token
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Register command and message handlers
    app.add_handler(start_handler)         # /start
    app.add_handler(feedback_handler)      # /feedback conversation
    app.add_handler(mood_handler)          # mood logs like "i dey stress"
    app.add_handler(intent_handler)        # intent/emotion detection
    app.add_handler(daily_handler)

    # Optional: Use polling for local testing
    if os.getenv("USE_POLLING") == "true":
        await app.run_polling()

def get_app():
    return app
