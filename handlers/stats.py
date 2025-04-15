from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import csv
from collections import Counter

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("logs/mood_log.csv", newline='') as file:
            moods = [row[2] for row in csv.reader(file)]
            count = Counter(moods)
            msg = "📊 Mood Stats:\n"
            for mood, num in count.items():
                msg += f"{mood}: {num}\n"
            await update.message.reply_text(msg)
    except FileNotFoundError:
        await update.message.reply_text("No stats yet.")

stats_handler = CommandHandler("stats", stats)
