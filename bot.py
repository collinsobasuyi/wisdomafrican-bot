from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters, CallbackContext
)
from dotenv import load_dotenv
import openai
import os
import logging
import csv
from datetime import datetime, time

# === ENV SETUP ===
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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
logger = logging.getLogger(__name__)

# === GLOBAL ===
user_ids = set()  # Add user ID when user interacts

MOOD_OPTIONS = [
    ["I dey stress 😩", "I no happy 😢"],
    ["I dey okay 😊", "I just wan yarn 🗣️"]
]

proverbs = {
    "i dey stress": "Even rain wey fall no dey last forever. Rest small, my pikin.",
    "i no happy": "Tears no fit cook yam. Tomorrow go better.",
    "i dey okay": "As breeze blow, fowl yansh go show — always be ready.",
    "i just wan yarn": "Talk wetin dey your chest. Mind no suppose carry load alone."
}

# === HELPERS ===
def log_mood(user_name, mood):
    with open("mood_log.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), user_name, mood])

def log_feedback(user_name, feedback_text):
    with open("feedback_log.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), user_name, feedback_text])

# === BOT HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)

    welcome_message = (
        "👋🏿 Welcome to *WisdomAfrican Bot*! \n\n"
        "I be your wise companion wey sabi give you African proverbs, calm words, and small small encouragement.\n\n"
        "Just tell me how you dey feel or ask me wetin dey worry you."
    )
    reply_markup = ReplyKeyboardMarkup(MOOD_OPTIONS, resize_keyboard=True)
    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    user_name = update.effective_user.first_name or "Unknown"
    user_id = update.effective_user.id
    user_ids.add(user_id)

    logging.info(f"User: {user_name} | Message: {user_text}")

    for key in proverbs:
        if key in user_text:
            response = proverbs[key]
            log_mood(user_name, key)
            break
    else:
        response = await generate_openai_response(user_text)

    await update.message.reply_text(response)

async def generate_openai_response(text):
    system_prompt = (
        "You are an African elder who speaks in Nigerian Pidgin and proverbs. "
        "Offer wise, calming, and respectful advice rooted in African tradition. "
        "Keep messages short and deeply comforting."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Unknown"
    feedback_text = " ".join(context.args)

    if not feedback_text:
        await update.message.reply_text("Type your feedback like this:\n/feedback I like this bot!")
        return

    log_feedback(user_name, feedback_text)
    await update.message.reply_text("Thanks for your feedback 🙏🏽")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("mood_log.csv", newline='') as file:
            reader = csv.reader(file)
            moods = [row[2] for row in reader]
            from collections import Counter
            counts = Counter(moods)

            message = "📊 *Mood Stats*\n"
            for mood, count in counts.items():
                message += f"{mood.title()}: {count}\n"
            await update.message.reply_text(message, parse_mode="Markdown")
    except FileNotFoundError:
        await update.message.reply_text("No mood data found yet.")

# === DAILY PROVERB PUSH ===
async def send_daily_proverb(context: CallbackContext):
    proverb = "No matter how hot your anger be, e no go cook yam. 🔥"
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=proverb)
        except Exception as e:
            logging.warning(f"Failed to send to {user_id}: {e}")

# === ERROR HANDLING ===
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling update:", exc_info=context.error)

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feedback", feedback))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    # Daily job at 9:00 AM
    app.job_queue.run_daily(send_daily_proverb, time=time(hour=9, minute=0))

    app.run_polling()
