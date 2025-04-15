import random
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

TONE_TAGS = [
    "my dear",
    "my personal person",
    "my friend",
    "my person",
    "my own person",
    "my oga"
]

def get_friendly_tag():
    return random.choice(TONE_TAGS)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    tone = get_friendly_tag()

    welcome_message = (
        f"Welcome, {tone}!\n\n"
        f"I'm Wisdom African Bot — built to share comfort, insight, and laughter with you.\n\n"
        f"You fit tell me how you dey feel, like:\n"
        f"`i dey stress` or `i no happy`\n\n"
        f"Na from our culture wisdom dey flow. Let's talk — I dey here for you."
    )

    await update.message.reply_text(welcome_message)

start_handler = CommandHandler("start", start_command)
