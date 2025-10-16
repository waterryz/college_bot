import os

# === ТВОЙ TELEGRAM TOKEN ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # добавь в Render Environment

# === ДОМЕН Render (после деплоя вставь сюда свой URL) ===
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app.onrender.com/webhook")

# === URL сайта колледжа ===
COLLEGE_URL = "https://college.snation.kz"

