import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from parser import get_grades
from db import init_db, save_credentials, get_credentials
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ Укажи BOT_TOKEN в Render Environment Variables!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Сәлем! / Привет!\n\n"
        "Бұл бот Snation College сайтындағы журналдан бағаларды көрсетеді.\n"
        "Чтобы начать, отправь свой ИИН и пароль через пробел:\n\n"
        "_Пример:_ `123456789012 12345678`",
        parse_mode="Markdown"
    )


@dp.message()
async def handle_login(message: types.Message):
    """Основная логика: принимает ИИН и пароль, проверяет, сохраняет, парсит оценки"""
    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            await message.answer("⚠️ Введи ИИН и пароль через пробел.\nПример: `123456789012 12345678`", parse_mode="Markdown")
            return

        iin, password = parts
        user_id = message.from_user.id

        await message.answer("🔄 Қосылуда... / Подключаюсь к сайту SmartNation...")

        result = get_grades(iin, password)

        if "❌" in result or "⚠️" in result:
            await message.answer(result)
            return

        save_credentials(user_id, iin, password)
        await message.answer(result, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"⚠️ Қате орын алды / Произошла ошибка: {e}")


async def main():
    print("🤖 Бот успешно запущен (polling mode)...")
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
