from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from db import init_db
from config import BOT_TOKEN, WEBHOOK_URL
from bot import router

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

@app.on_event("startup")
async def on_startup():
    init_db()
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set successfully!")

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_raw_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "running"}
