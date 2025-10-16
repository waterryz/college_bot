from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from bot import dp, bot

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook("https://college-bot-x3wx.onrender.com/webhook")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await dp.feed_raw_update(bot, data)
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "running"}
