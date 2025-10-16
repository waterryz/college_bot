from fastapi import FastAPI, Request
import asyncio
from aiogram import Bot, Dispatcher
from bot import dp, bot
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook("https://your-app.onrender.com/webhook")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await dp.feed_update(bot, data)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)

