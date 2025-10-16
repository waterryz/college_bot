from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
import json, os
from parser import get_grades

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

from aiogram import Router, types
from parser import get_grades_from_html

router = Router()

@router.message(commands=["grades"])
async def send_grades(message: types.Message):
    with open("Журнал.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    result = get_grades_from_html(html_content)
    await message.answer(result, parse_mode="Markdown")


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет 👋\nОтправь логин и пароль через пробел.\nПример:\n`ivan123 mypassword`", parse_mode="Markdown")

@dp.message(F.text)
async def save_credentials(message: types.Message):
    users = load_users()
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("Формат неверен. Отправь логин и пароль через пробел.")
        return
    login, password = parts
    users[str(message.from_user.id)] = {"login": login, "password": password}
    save_users(users)
    await message.answer("✅ Данные сохранены! Теперь введи /grades чтобы получить оценки.")

@dp.message(Command("grades"))
async def grades(message: types.Message):
    users = load_users()
    if str(message.from_user.id) not in users:
        await message.answer("⚠️ Сначала введи логин и пароль (см. /start).")
        return
    creds = users[str(message.from_user.id)]
    result = get_grades(creds["login"], creds["password"])

    if "error" in result:
        await message.answer(f"❌ {result['error']}")
        return

    text = "📚 *Твои оценки:*\n\n" + "\n".join([f"• {s}: {g}" for s, g in result["grades"]])
    await message.answer(text, parse_mode="Markdown")
