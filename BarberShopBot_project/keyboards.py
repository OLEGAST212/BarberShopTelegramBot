
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def contact_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для запроса и отправки номера."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Поделиться номером", request_contact=True)]],
        one_time_keyboard=True,
        resize_keyboard=True
    )

def remove_keyboard() -> ReplyKeyboardRemove:
    """Убрать пользовательскую клавиатуру."""
    return ReplyKeyboardRemove()
