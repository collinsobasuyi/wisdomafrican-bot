import os
import datetime
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

# Feedback conversation states
ASKING_FEEDBACK = 1

# Ensure log folder exists
def log_feedback(user, message):
    os.makedirs("logs", exist_ok=True)
    with open("logs/feedback_log.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{user},{message}\n")

# Start feedback collection
async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I dey hear you, my person 🙏\n\nPlease reply with any feedback or suggestion you wan share."
    )
    return ASKING_FEEDBACK

# Handle the actual feedback message
async def feedback_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    feedback_text = update.message.text

    log_feedback(user, feedback_text)

    await update.message.reply_text("Thank you for your feedback, my dear! I don jot am down.")
    return ConversationHandler.END

# Handle cancellation (optional)
async def cancel_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("No wahala! You fit give feedback anytime.")
    return ConversationHandler.END

# Feedback handler setup
feedback_handler = ConversationHandler(
    entry_points=[CommandHandler("feedback", feedback_start)],
    states={
        ASKING_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_received)],
    },
    fallbacks=[CommandHandler("cancel", cancel_feedback)]
)
