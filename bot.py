from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import openai
import os
import logging
import csv
from datetime import datetime

# === ENVIRONMENT SETUP ===
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === OPENAI CLIENT ===
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# === LOGGING SETUP ===
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("afrobot.log"),
        logging.StreamHandler()
    ]
)

# === MOOD OPTIONS ===
MOOD_OPTIONS = [
    ["I dey stress 😩", "I no happy 😢"],
    ["I dey okay 😊", "I just wan yarn 🗣️"]
]

# === PREDEFINED RESPONSES ===
proverbs = {
    "i dey stress": "Even rain wey fall no dey last forever. Rest small, my pikin.",
    "i no happy": "Tears no fit cook yam. Tomorrow go better.",
    "i dey okay": "As breeze blow, fowl yansh go show — always be ready.",
    "i just wan yarn": "Talk wetin dey your chest. Mind no suppose carry load alone."
}

# === MOOD LOGGING ===
def log_mood(user_name, mood):
    with open("mood_log.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), user_name, mood])

# === BOT COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MOOD_OPTIONS, resize_keyboard=True)
    await update.message.reply_text("Wetin dey worry you small today? Choose one 👇🏽", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    user_name = update.effective_user.first_name or "Unknown"

    logging.info(f"User: {user_name} | Message: {user_text}")

    for key in proverbs:
        if key in user_text:
            response = proverbs[key]
            log_mood(user_name, key)
            logging.info(f"Custom proverb sent for mood: {key}")
            break
    else:
        response = await generate_openai_response(user_text)
        logging.info("Used OpenAI fallback")

    await update.message.reply_text(response)

async def generate_openai_response(text):
    prompt = f"You be wise African elder. Reply to this person in Nigerian Pidgin with kind words or proverbs: {text}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You be gentle African elder. Talk for Nigerian Pidgin and use African proverbs. Keep message kind and short."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# === RUN BOT ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
