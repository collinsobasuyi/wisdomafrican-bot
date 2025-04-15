import os
import datetime
import random
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters

# INTENT RESPONSES
INTENTS = {
    "stress": {
        "keywords": ["stress", "overwhelmed", "tired", "work", "burn out", "exhausted"],
        "response": [
            "Even rain no dey fall forever. Rest small, my dear.",
            "Body no be machine. Try pause, breathe small.",
            "Wahala no dey finish — na you suppose finish am."
        ]
    },
    "sadness": {
        "keywords": ["sad", "lonely", "cry", "depressed", "down", "nobody", "hurt"],
        "response": [
            "Tears no fit cook yam. Tomorrow go better, my person.",
            "Even darkest night get morning. You no dey alone.",
            "When heart heavy, talk small. I dey listen."
        ]
    },
    "anxiety": {
        "keywords": ["anxious", "panic", "fear", "scared", "overthink", "worried", "nervous"],
        "response": [
            "No carry tomorrow worry enter today, my personal person.",
            "Slow down. Even tortoise dey reach him destination.",
            "Hold ground, breathe deep. Storm go pass."
        ]
    },
    "vent": {
        "keywords": ["talk", "vent", "share", "yarn", "speak", "rant", "express"],
        "response": [
            "Talk your mind, my dear. I dey hear you.",
            "Mind no suppose carry load alone. Yarn wetin dey.",
            "Na talk dey clear chest. Go ahead, I dey here."
        ]
    }
}

# SELF-CARE ACTIONS
ACTIONS = {
    "stress": [
        "Try this: pause what you dey do, breathe in 3 times, slowly. Your peace matters.",
        "Step outside for 2 minutes. Let your body know say you safe."
    ],
    "sadness": [
        "Try write one small thing wey make you smile this week. Gratitude dey heal slowly.",
        "Call person wey dey always make you laugh — even if na just 2 minutes."
    ],
    "anxiety": [
        "Hold something in your hand, feel the texture. Focus on it. This be grounding.",
        "Say this: 'I am safe. I am not my worry.' Repeat am two times."
    ],
    "vent": [
        "You talk well. If you wan yarn more, I dey here.",
        "Next time e heavy, write am down. Journaling dey help mind rest."
    ]
}

def detect_intent(user_text):
    """Check message text for any keywords matching intent."""
    text = user_text.lower()
    for intent, data in INTENTS.items():
        for keyword in data["keywords"]:
            if keyword in text:
                return intent
    return None

def get_random_response(intent):
    return random.choice(INTENTS[intent]["response"])

def get_random_action(intent):
    return random.choice(ACTIONS[intent])

def log_mood(user, intent):
    os.makedirs("logs", exist_ok=True)
    with open("logs/mood_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{user},{intent}\n")

# Final handler
async def handle_emotion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user.first_name

    intent = detect_intent(text)

    if intent:
        log_mood(user, intent)
        response = get_random_response(intent)
        action = get_random_action(intent)
        full_reply = f"{response}\n\n{action}"
        await update.message.reply_text(full_reply)
    else:
        await update.message.reply_text("I hear you, my person. Say more if you like — I dey here.")

# Telegram handler
intent_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_emotion)
