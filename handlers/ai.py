# handlers/ai.py
from telegram import Update
from telegram.ext import ContextTypes
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ai_response_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a warm, supportive African mental health companion. Reply with empathy, mix in African cultural wisdom, and provide emotional support when needed."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        await update.message.reply_text("Hmm, something go wrong. Try again small time.")
