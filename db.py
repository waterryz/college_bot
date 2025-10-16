import sqlite3
from cryptography.fernet import Fernet

from config import ENCRYPTION_KEY

f = Fernet(ENCRYPTION_KEY)

def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        user_id INTEGER PRIMARY KEY,
        login TEXT,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_credentials(user_id, login, password):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    encrypted = f.encrypt(password.encode()).decode()
    c.execute("REPLACE INTO students (user_id, login, password) VALUES (?, ?, ?)",
              (user_id, login, encrypted))
    conn.commit()
    conn.close()

def get_credentials(user_id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT login, password FROM students WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], f.decrypt(row[1].encode()).decode()
    return None, None
