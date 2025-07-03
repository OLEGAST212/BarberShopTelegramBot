from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import WEB_APP_URL

def contact_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для запроса и отправки номера."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Поделиться номером", request_contact=True)]],
        one_time_keyboard=True,
        resize_keyboard=True
    )


def web_app_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text="qoob/Личный кабинет",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]],

    )
def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
