import openai
import random
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """
You are an emotionally intelligent African mental health companion.
You speak with warmth and wisdom, using mostly English and occasional Nigerian Pidgin to sound relatable and friendly.

Always respond with empathy. When someone is sad, stressed, or lonely, comfort them gently. Ask thoughtful questions and encourage helpful actions like breathing, journaling, or rest.

Only use African proverbs when it fits the emotion — not every time.
"""

async def generate_empathetic_response(user_input):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Error generating response:", e)
        fallback = random.choice([
            "I hear you, my dear. Want to talk more about how you’re feeling?",
            "You dey strong — I see you. Let’s take it one step at a time.",
            "Even on cloudy days, the sun still dey shine somewhere. You’re not alone."
        ])
        return fallback
