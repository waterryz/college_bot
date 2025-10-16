import sqlite3
from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            login TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_credentials(user_id, login, password):
    cipher = Fernet(ENCRYPTION_KEY)
    enc_login = cipher.encrypt(login.encode()).decode()
    enc_password = cipher.encrypt(password.encode()).decode()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("REPLACE INTO users (user_id, login, password) VALUES (?, ?, ?)", (user_id, enc_login, enc_password))
    conn.commit()
    conn.close()

def get_credentials(user_id):
    cipher = Fernet(ENCRYPTION_KEY)

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT login, password FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        login = cipher.decrypt(row[0].encode()).decode()
        password = cipher.decrypt(row[1].encode()).decode()
        return login, password
    return None, None
