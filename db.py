import sqlite3
from config import fernet

def init_db():
    conn = sqlite3.connect("users.db", check_same_thread=False)
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
    conn = sqlite3.connect("users.db", check_same_thread=False)
    c = conn.cursor()
    enc_login = fernet.encrypt(login.encode()).decode()
    enc_password = fernet.encrypt(password.encode()).decode()
    c.execute("""
        REPLACE INTO users (user_id, login, password)
        VALUES (?, ?, ?)
    """, (user_id, enc_login, enc_password))
    conn.commit()
    conn.close()


def get_credentials(user_id):
    conn = sqlite3.connect("users.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT login, password FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        login = fernet.decrypt(row[0].encode()).decode()
        password = fernet.decrypt(row[1].encode()).decode()
        return login, password
    return None, None
