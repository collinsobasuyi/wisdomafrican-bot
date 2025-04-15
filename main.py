from fastapi import FastAPI, Request
from telegram import Update
import uvicorn
import asyncio
import logging

from bot import setup_bot, get_app

logging.basicConfig(level=logging.INFO)
fastapi_app = FastAPI()

@fastapi_app.on_event("startup")
async def startup():
    await setup_bot()

@fastapi_app.post("/")
async def telegram_webhook(req: Request):
    app = get_app()
    if not app:
        return {"error": "App not ready"}
    data = await req.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return {"ok": True"}

if __name__ == "__main__":
    asyncio.run(uvicorn.run("main:fastapi_app", host="0.0.0.0", port=10000))
