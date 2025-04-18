import os
import uvicorn
import nest_asyncio
from fastapi import FastAPI, Request
from telegram import Update
from bot import setup_bot, get_app

# Initialize FastAPI app
fastapi_app = FastAPI()

# Run setup_bot on startup
@fastapi_app.on_event("startup")
async def startup():
    await setup_bot()

# Webhook endpoint
@fastapi_app.post("/")
async def webhook_handler(request: Request):
    app = get_app()
    if app is None:
        print("⚠️ Bot not initialized yet.")
        return {"error": "Bot app not ready."}

    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return {"ok": True}

# Run locally if needed
if __name__ == "__main__":
    nest_asyncio.apply()
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:fastapi_app", host="0.0.0.0", port=port)
