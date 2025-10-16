import os
from cryptography.fernet import Fernet

# Токен телеграм-бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ключ шифрования для базы
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)
