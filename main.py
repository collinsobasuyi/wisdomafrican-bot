import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update
import nest_asyncio
import uvicorn
from bot import setup_bot, get_app

fastapi_app = FastAPI()

@fastapi_app.on_event("startup")
async def startup():
    await setup_bot()

@fastapi_app.post("/")
async def webhook(req: Request):
    app = get_app()
    if app is None:
        return {"error": "App not ready"}
    update = Update.de_json(await req.json(), app.bot)
    await app.process_update(update)
    return {"ok": True}

if __name__ == "__main__":
    nest_asyncio.apply()
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:fastapi_app", host="0.0.0.0", port=port)
