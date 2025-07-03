from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from BarberShopBot_project.db import is_registered, ensure_user, register_user
from BarberShopBot_project.keyboards import contact_keyboard, remove_keyboard, web_app_inline_keyboard
from BarberShopBot_project.texts import WELCOME_NEW, WELCOME_BACK, USER_NOTIFICATION, WELCOME_BACK_2

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_registered(user_id):
        # Уже зарегистрирован
        await update.message.reply_text(
            WELCOME_BACK,
            reply_markup=web_app_inline_keyboard()
        )
        await update.message.reply_text(WELCOME_BACK_2, reply_markup=remove_keyboard())
        await update.message.reply_text(USER_NOTIFICATION, reply_markup=remove_keyboard())
    else:
        # Новичок: создаём запись и просим номер
        ensure_user(user_id)
        await update.message.reply_text(
            WELCOME_NEW,
            reply_markup=contact_keyboard()
        )

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.effective_user.id
    register_user(user_id, contact.phone_number)
    await update.message.reply_text(
        f"Спасибо! Вы зарегистрированы под номером {contact.phone_number}.",
        reply_markup=remove_keyboard()
    )
    # Показываем личный кабинет
    await update.message.reply_text(
        WELCOME_BACK,
        reply_markup=web_app_inline_keyboard()
    )
    await update.message.reply_text(WELCOME_BACK_2, reply_markup=remove_keyboard())
    await update.message.reply_text(USER_NOTIFICATION, reply_markup=remove_keyboard())


def register_auth_handlers(app):
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
