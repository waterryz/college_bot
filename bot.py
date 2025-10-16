from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message
from db import init_db, save_credentials, get_credentials
from parser import get_grades

router = Router()
pending_login = {}
pending_password = {}

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет! Я помогу тебе посмотреть твои оценки.\n"
        "👋 Сәлем! Мен сенің бағаларыңды көрсетемін.\n\n"
        "🆔 Введи свой *ЖСН (ИИН)* номер:\n"
        "🆔 Өзінің *ЖСН (ИИН)* нөміріңді енгіз:"
    )
    pending_login[message.from_user.id] = True

@router.message(lambda m: pending_login.get(m.from_user.id))
async def handle_login(message: Message):
    user_id = message.from_user.id
    pending_login.pop(user_id, None)
    pending_password[user_id] = message.text.strip()
    await message.answer(
        "🔒 Теперь введи свой *пароль*:\n"
        "🔒 Енді өзіңнің *құпия сөзіңді* енгіз:"
    )

@router.message(lambda m: pending_password.get(m.from_user.id))
async def handle_password(message: Message):
    user_id = message.from_user.id
    login = pending_password.pop(user_id)
    password = message.text.strip()

    save_credentials(user_id, login, password)
    await message.answer(
        "✅ Данные сохранены! Теперь можешь написать /grades чтобы увидеть свои оценки.\n"
        "✅ Мәліметтер сақталды! Енді /grades деп жаз — бағаларыңды көру үшін."
    )

@router.message(Command("grades"))
async def grades_handler(message: Message):
    login, password = get_credentials(message.from_user.id)
    if not login:
        await message.answer(
            "⚠️ Сначала введи ЖСН и пароль командой /start.\n"
            "⚠️ Алдымен /start арқылы ЖСН және құпия сөз енгіз."
        )
        return

    await message.answer(
        "⏳ Загружаю твои оценки...\n"
        "⏳ Бағаларыңыз жүктелуде..."
    )
    result = get_grades(login, password)
    await message.answer(result, parse_mode="Markdown")
