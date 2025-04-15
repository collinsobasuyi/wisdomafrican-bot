from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import csv
from datetime import datetime

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    message = " ".join(context.args)
    with open("logs/feedback_log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user, message])
    await update.message.reply_text("Thanks for your feedback 🙏🏾")

feedback_handler = CommandHandler("feedback", feedback)
