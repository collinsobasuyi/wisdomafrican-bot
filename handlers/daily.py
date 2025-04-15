from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters
import datetime
import os

# Mood options
MOODS = {
    "I dey stress": "Even rain no dey fall forever. Rest small, my dear.",
    "I feel sad": "Tears no fit cook yam. Tomorrow go better.",
    "I dey okay": "Even when sun shine, breeze fit still blow. You dey do well.",
    "I feel calm": "Water wey calm pass fit still deep. Enjoy your peace.",
    "I no sabi": "No wahala. Feelings no dey always get name. Just breathe small."
}

SELECTING = 1

def save_mood(user, mood):
    os.makedirs("logs", exist_ok=True)
    with open("logs/mood_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{user},{mood}\n")

# Step 1: Start check-in
async def start_daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(mood)] for mood in MOODS.keys()]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("How you dey feel today? Pick one small:", reply_markup=markup)
    return SELECTING

# Step 2: Handle user response
async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mood = update.message.text
    user = update.effective_user.first_name

    if mood in MOODS:
        proverb = MOODS[mood]
        save_mood(user, mood)
        await update.message.reply_text(f"{proverb}\n\nThanks for checking in today.")
    else:
        await update.message.reply_text("I no fit understand that one. Try pick from the buttons.")

    return ConversationHandler.END

# Step 3: Cancel flow
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("No wahala. You fit try again later.")
    return ConversationHandler.END

# Build handler
daily_handler = ConversationHandler(
    entry_points=[CommandHandler("daily", start_daily)],
    states={SELECTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mood)]},
    fallbacks=[CommandHandler("cancel", cancel)],
)
