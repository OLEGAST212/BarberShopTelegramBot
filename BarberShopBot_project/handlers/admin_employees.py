from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from BarberShopBot_project.config import ADMIN_CHAT_ID
from BarberShopBot_project.db import add_employee

# Состояния разговора
ASK_NAME, ASK_PHONE = range(2)

async def add_emp_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # команда доступна только админу
    if update.effective_user.id != ADMIN_CHAT_ID:
        return
    await update.message.reply_text("Введите имя нового сотрудника:")
    return ASK_NAME

async def add_emp_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["new_emp_name"] = update.message.text.strip()
    await update.message.reply_text(
        "Теперь введите телефон сотрудника (или напишите «нет»):"
    )
    return ASK_PHONE

async def add_emp_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = update.message.text.strip()
    phone = None if raw.lower() in ("нет", "-") else raw
    name = context.user_data["new_emp_name"]
    emp_id = add_employee(name, phone)
    await update.message.reply_text(
        f"✅ Сотрудник #{emp_id} «{name}» добавлен" +
        (f" с телефоном {phone}" if phone else "")
    )
    return ConversationHandler.END

async def add_emp_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добавление сотрудника отменено.")
    return ConversationHandler.END

def register_admin_employee_handlers(app):
    conv = ConversationHandler(
        entry_points=[CommandHandler("add_employee", add_emp_start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_emp_name)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_emp_phone)],
        },
        fallbacks=[CommandHandler("cancel", add_emp_cancel)],
    )
    app.add_handler(conv)
