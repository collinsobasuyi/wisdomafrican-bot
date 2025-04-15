from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from services.openai_chat import get_ai_response
import csv
from datetime import datetime

proverbs = {
    "i dey stress": "Even rain wey fall no dey last forever. Rest small, my pikin.",
    "i no happy": "Tears no fit cook yam. Tomorrow go better.",
    "i dey okay": "As breeze blow, fowl yansh go show — always be ready.",
    "i just wan yarn": "Talk wetin dey your chest. Mind no suppose carry load alone."
}

def log_mood(user, mood):
    with open("logs/mood_log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user, mood])

async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user.first_name
    for key in proverbs:
        if key in text:
            log_mood(user, key)
            await update.message.reply_text(proverbs[key])
            return
    # fallback to OpenAI
    reply = await get_ai_response(text)
    await update.message.reply_text(reply)

mood_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mood)
