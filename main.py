import os
import uvicorn
import nest_asyncio
from fastapi import FastAPI, Request
from telegram import Update
from bot import setup_bot, get_app
from dotenv import load_dotenv

load_dotenv()

fastapi_app = FastAPI()
app = None  # will hold the Telegram bot application instance

@fastapi_app.on_event("startup")
async def startup():
    global app
    await setup_bot()
    app = get_app()
    await app.initialize()  # REQUIRED for webhook mode
    await app.start()       # REQUIRED for webhook mode

@fastapi_app.post("/")
async def webhook_handler(request: Request):
    global app
    if app is None:
        print("App not initialized yet.")
        return {"error": "Bot app not ready."}

    data = await request.json()
    update = Update.de_json(data, app.bot)

    try:
        await app.process_update(update)
    except Exception as e:
        print("Error in webhook_handler:", e)

    return {"ok": True}

if __name__ == "__main__":
    nest_asyncio.apply()
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:fastapi_app", host="0.0.0.0", port=port)
