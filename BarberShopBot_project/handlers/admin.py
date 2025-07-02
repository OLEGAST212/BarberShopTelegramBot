import re
from telegram import Update
from telegram.ext import (
    MessageHandler,
    ContextTypes,
    filters,
)
from BarberShopBot_project.config import ADMIN_CHAT_ID, ADMIN_THREAD_ID_1
from telegram.helpers import escape_markdown

async def admin_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # 1) Работаем только в админ-чате
    if msg.chat.id != ADMIN_CHAT_ID:
        return
    # 1.1) И только в нужной теме (thread)
    if msg.message_thread_id != ADMIN_THREAD_ID_1:
        return
    # 2) Только replies — админ «ответил» на наше уведомление
    if not msg.reply_to_message:
        return
    orig = msg.reply_to_message.text or ""
    # Ищем ID пользователя в тексте вида "ID: 12345678"
    match = re.search(r"ID:\s*(\d+)", orig)
    if not match:
        return

    user_id = int(match.group(1))
    admin_label = escape_markdown("Администратор", version=2)
    reply = escape_markdown(msg.text, version=2)


    # Шлём ответ обратно пользователю
    await context.bot.send_message(
        chat_id=user_id,
        text=f"*{admin_label}*:\n{reply}",
        parse_mode="MarkdownV2"
    )
def register_admin_handlers(app):
    app.add_handler(
        MessageHandler(
            filters.Chat(ADMIN_CHAT_ID) & filters.TEXT & filters.REPLY,
            admin_reply_handler
        ),
        group=1
    )