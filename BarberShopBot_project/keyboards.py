# BarberShopBot_project/keyboards.py

from urllib.parse import urlencode
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    WebAppInfo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import WEB_APP_URL

def contact_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для запроса и отправки номера."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Поделиться номером", request_contact=True)]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def web_app_inline_keyboard(phone: str | None = None) -> InlineKeyboardMarkup:
    """
    Inline‑клавиатура для запуска WebApp.
    Если передан phone, он будет добавлен как GET‑параметр ?phone=... к URL.
    """
    url = WEB_APP_URL
    if phone:
        # Преобразуем номер в валидный GET‑параметр
        url = f"{WEB_APP_URL}?{urlencode({'phone': phone})}"

    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text="qoob/Личный кабинет",
                web_app=WebAppInfo(url=url)
            )
        ]]
    )

def remove_keyboard() -> ReplyKeyboardRemove:
    """Убирает Reply‑клавиатуру."""
    return ReplyKeyboardRemove()
