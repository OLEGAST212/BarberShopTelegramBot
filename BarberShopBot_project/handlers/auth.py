# handlers/auth.py

import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

from BarberShopBot_project.db import (
    is_registered,
    ensure_user,
    register_user,
    get_profile,
    save_profile,
)
from BarberShopBot_project.keyboards import (
    contact_keyboard,
    remove_keyboard,
    web_app_reply_keyboard,
)
from BarberShopBot_project.texts import (
    WELCOME_NEW,
    WELCOME_BACK,
    WELCOME_BACK_2,
    USER_NOTIFICATION,
)

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_registered(user_id):
        profile = get_profile(user_id)
        logger.info("▶️ Профиль из БД при старте: %s", profile)

        await update.message.reply_text(
            WELCOME_BACK,
            reply_markup=web_app_reply_keyboard(profile)
        )
        await update.message.reply_text(WELCOME_BACK_2)
        await update.message.reply_text(USER_NOTIFICATION)

    else:
        ensure_user(user_id)
        await update.message.reply_text(
            WELCOME_NEW,
            reply_markup=contact_keyboard()
        )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.effective_user.id

    register_user(user_id, contact.phone_number)
    # Сразу сохраняем телефон в профиле
    save_profile(telegram_id=user_id, phone=contact.phone_number)

    logger.info("▶️ Профиль после регистрации: %s", get_profile(user_id))

    await update.message.reply_text(
        f"Спасибо! Зарегистрированы под номером {contact.phone_number}.",
        reply_markup=remove_keyboard()
    )
    # Показываем форму с уже заполненным телефоном
    profile = get_profile(user_id)
    await update.message.reply_text(
        WELCOME_BACK,
        reply_markup=web_app_reply_keyboard(profile)
    )
    await update.message.reply_text(WELCOME_BACK_2)
    await update.message.reply_text(USER_NOTIFICATION)

def register_auth_handlers(app):
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
