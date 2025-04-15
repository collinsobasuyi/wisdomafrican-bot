import os
import datetime
import random
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from services.openai_chat import get_ai_response

# Specific keyword-matching proverbs
PROVERBS = {
    "i dey stress": "Even rain wey fall no dey last forever. Rest small",
    "i no happy": "Tears no fit cook yam. Tomorrow go better",
    "i dey okay": "As breeze blow, fowl yansh go show — always be ready",
    "i just wan yarn": "Talk wetin dey your chest. Mind no suppose carry load alone"
}

# Extra proverbs (fallback random list)
EXTRA_PROVERBS = [
    "No be every frog wey jump na get destination — take am easy",
    "If soup sweet, na money kill am — try rest before you cook too much wahala",
    "Na who no get slipper dey run first — slow down small",
    "Even tortoise dey reach him destination — one step at a time",
    "Na from clap dance dey start — no let small wahala turn to big fight",
    "Who no dey inside pot no suppose say soup no hot — be kind to others",
    "If breeze blow, fowl yansh go show — truth no dey hide forever",
    "Monkey wey no get tail no dey climb tree — choose your battles wisely",
    "No be who first call police dey win case — calm down",
    "If you run pass your shadow, na juju be that — chill small",
    "Coconut head sometimes need soft palm — bend small, no break",
    "If e no be panadol, e no fit be like panadol — stay original",
    "Even jollof rice dey burn if you no watch am — stay present",
    "When mosquito dey sing for your ear, na reminder say peace no cheap",
    "E no go better for poverty — so rest and hustle wisely",
    "No use today finish tomorrow's energy — rest no be laziness",
    "Person wey wan swallow egg go check him throat first — think well",
    "Lizard nod head, e dey thank God say e fall land — celebrate your small wins",
    "Fish wey dey look up dey learn how to climb — keep aiming high",
    "Wahala no dey finish — enjoy small before next round show"
]

# Warm Nigerian closings
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

def log_mood(user, mood):
    os.makedirs("logs", exist_ok=True)
    with open("logs/mood_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{user},{mood}\n")

def get_random_proverb():
    return f"{random.choice(EXTRA_PROVERBS)}, {get_friendly_tag()}."

async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user.first_name

    # Check for keyword-based match
    for key in PROVERBS:
        if key in text:
            log_mood(user, key)
            response = f"{PROVERBS[key]}, {get_friendly_tag()}."
            await update.message.reply_text(response)
            return

    # Fallback to random funny proverb
    log_mood(user, text)
    await update.message.reply_text(get_random_proverb())

# Register handler
mood_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mood)
