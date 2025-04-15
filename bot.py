import os
from telegram.ext import ApplicationBuilder
from handlers.start import start_handler
from handlers.feedback import feedback_handler
from handlers.mood import mood_handler

# Global bot application
app = None

async def setup_bot():
    global app

    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add all handlers
    app.add_handler(start_handler)
    app.add_handler(feedback_handler)
    app.add_handler(mood_handler)

    # Optionally run polling if local
    if os.getenv("USE_POLLING") == "true":
        await app.run_polling()

def get_app():
    return app
