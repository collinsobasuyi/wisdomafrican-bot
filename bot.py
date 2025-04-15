import os
import nest_asyncio
import asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from handlers.start import start_handler
from handlers.mood import mood_handler
from handlers.feedback import feedback_handler
from handlers.stats import stats_handler

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = None

async def setup_bot():
    global app
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(mood_handler)
    app.add_handler(feedback_handler)
    app.add_handler(stats_handler)
    await app.initialize()
    await app.bot.set_webhook(WEBHOOK_URL)
    return app

# used by main.py
def get_app():
    return app
