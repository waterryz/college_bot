import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "default_key").encode()
