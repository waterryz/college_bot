import os
from cryptography.fernet import Fernet

# 🔑 Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔐 Ключ шифрования для users.db
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    # Если ключа нет — создаем новый и подсказываем добавить его в Render
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print("⚠️ Новый ENCRYPTION_KEY сгенерирован! Скопируй и добавь в Render ENV:")
    print(ENCRYPTION_KEY)

fernet = Fernet(ENCRYPTION_KEY.encode())
