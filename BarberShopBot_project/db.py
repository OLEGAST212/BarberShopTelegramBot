
import sqlite3
from config import DB_PATH

# единственное соединение на всё приложение
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            phone TEXT,
            registered INTEGER DEFAULT 0
        )
    """)
    conn.commit()

def is_registered(user_id: int) -> bool:
    cursor.execute(
        "SELECT registered FROM users WHERE telegram_id = ?", (user_id,)
    )
    row = cursor.fetchone()
    return bool(row and row[0])

def ensure_user(user_id: int):
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (user_id,)
    )
    conn.commit()

def register_user(user_id: int, phone: str):
    ensure_user(user_id)
    cursor.execute("""
        UPDATE users
        SET phone = ?, registered = 1
        WHERE telegram_id = ?
    """, (phone, user_id))
    conn.commit()
