# handlers/echo.py
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from BarberShopBot_project.db import is_registered
from BarberShopBot_project.keyboards import remove_keyboard
from BarberShopBot_project.texts import NOT_REGISTERED
from BarberShopBot_project.config import ADMIN_CHAT_ID, ADMIN_THREAD_ID_1

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Игнорируем админ-чат
    if chat_id == ADMIN_CHAT_ID:
        return

    user = update.effective_user
    if not is_registered(user.id):
        await update.message.reply_text(
            NOT_REGISTERED,
            reply_markup=remove_keyboard()
        )
        return

    # Формируем текст для админа
    username_part = f" (@{user.username})" if user.username else ""
    admin_text = (
        f"📩 Сообщение от {user.full_name}{username_part}\n"
        f"ID: {user.id}\n\n"
        f"{update.message.text}"
    )

    # Отправляем как новое сообщение в нужную тему
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        message_thread_id=ADMIN_THREAD_ID_1,
        text=admin_text
    )



def register_echo_handlers(app):
    app.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND,
            echo_handler
        )
    )
