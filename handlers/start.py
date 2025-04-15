from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

MOOD_OPTIONS = [
    ["I dey stress 😩", "I no happy 😢"],
    ["I dey okay 😊", "I just wan yarn 🗣️"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋🏿 Welcome to WisdomAfrican Bot! How you dey?"
    reply_markup = ReplyKeyboardMarkup(MOOD_OPTIONS, resize_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

start_handler = CommandHandler("start", start)
