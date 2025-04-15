import openai
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_ai_response(text):
    prompt = (
        "You are a wise African elder who gives short advice in Nigerian Pidgin. "
        "Speak with calmness, rooted in proverbs and culture."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()
