# handlers/ai.py

from telegram import Update
from telegram.ext import ContextTypes
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def ai_response_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = update.effective_user.id

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a warm, supportive African mental health companion. Reply with empathy, mix in African cultural wisdom, and provide emotional support when needed."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"OpenAI error: {e}")
        await update.message.reply_text("Something went wrong while I was thinking. Try again soon.")
