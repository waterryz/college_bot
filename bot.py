from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from db import save_credentials, get_credentials
from parser import get_grades
import asyncio
import logging
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    login = State()
    password = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("👋 Привет! Я помогу тебе посмотреть твои оценки.\n\n"
                         "👋 Сәлем! Мен сенің бағаларыңды көрсетемін.\n\n"
                         "🆔 Введи свой *ЖСН (ИИН)* номер:\n"
                         "🆔 Өзінің *ЖСН (ИИН)* нөміріңді енгіз:")
    await state.set_state(Form.login)

@dp.message(Form.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("🔒 Теперь введи свой *пароль*:\n"
                         "🔒 Енді өзіңнің *құпия сөзіңді* енгіз:")
    await state.set_state(Form.password)

@dp.message(Form.password)
async def process_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    login = data["login"]
    password = message.text

    save_credentials(message.from_user.id, login, password)
    await state.clear()
    await message.answer("✅ Данные сохранены! Теперь можешь написать /grades чтобы увидеть свои оценки.\n"
                         "✅ Мәліметтер сақталды! Енді /grades деп жаз — бағаларыңды көру үшін.")

@dp.message(Command("grades"))
async def get_user_grades(message: types.Message):
    login, password = get_credentials(message.from_user.id)
    if not login or not password:
        await message.answer("⚠️ Сначала введи свой ИИН и пароль через /start.")
        return

    await message.answer("⏳ Загружаю твои оценки...\n⏳ Бағаларыңыз жүктелуде...")
    result = get_grades(login, password)
    await message.answer(result, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
