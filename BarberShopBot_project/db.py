
import sqlite3
from config import DB_PATH

# Открываем единственное соединение на всё приложение
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def init_db():
    """
    Создаёт все нужные таблицы, если их ещё нет:
     - users       — для хранения номера и статуса регистрации
     - profiles    — для данных из Web App (профиль клиента)
     - appointments— для записей на услуги
    """
    # Пользователи
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            phone        TEXT,
            registered   INTEGER DEFAULT 0
        )
    """)

    # Профили, заполняются из мини‑приложения
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            telegram_id INTEGER PRIMARY KEY,
            first_name  TEXT,
            last_name   TEXT,
            patronymic  TEXT,
            phone       TEXT,
            email       TEXT
        )
    """)

    # Записи на услуги
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER,
            service  TEXT,
            datetime TEXT
        )
    """)

    conn.commit()


def is_registered(user_id: int) -> bool:
    """
    Проверяет, зарегистрирован ли пользователь (flag registered == 1).
    """
    cursor.execute(
        "SELECT registered FROM users WHERE telegram_id = ?", (user_id,)
    )
    row = cursor.fetchone()
    return bool(row and row[0])


def ensure_user(user_id: int):
    """
    Создаёт пустую запись для нового пользователя, если её ещё нет.
    """
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()

def get_user_phone(user_id: int) -> str | None:
    cursor.execute("SELECT phone FROM users WHERE telegram_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def register_user(user_id: int, phone: str):
    """
    Отмечает пользователя как зарегистрированного и сохраняет телефон.
    """
    ensure_user(user_id)
    cursor.execute("""
        UPDATE users
        SET phone = ?, registered = 1
        WHERE telegram_id = ?
    """, (phone, user_id))
    conn.commit()


def save_profile(
    telegram_id: int,
    first_name: str,
    last_name: str,
    patronymic: str,
    phone: str,
    email: str
):
    """
    Сохраняет или обновляет профиль пользователя из Web App.
    """
    cursor.execute("""
        INSERT INTO profiles
          (telegram_id, first_name, last_name, patronymic, phone, email)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
          first_name = excluded.first_name,
          last_name  = excluded.last_name,
          patronymic = excluded.patronymic,
          phone      = excluded.phone,
          email      = excluded.email
    """, (telegram_id, first_name, last_name, patronymic, phone, email))
    conn.commit()


def init_appointments_table():
    """
    Создаёт таблицу appointments, если она не была создана в init_db().
    (Можно вызывать отдельно, но обычно всё поднимается через init_db().)
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER,
            service  TEXT,
            datetime TEXT
        )
    """)
    conn.commit()


def save_appointment(user_id: int, service: str, dt: str):
    """
    Сохраняет новую запись на услугу.
    """
    cursor.execute(
        "INSERT INTO appointments (user_id, service, datetime) VALUES (?, ?, ?)",
        (user_id, service, dt)
    )
    conn.commit()
