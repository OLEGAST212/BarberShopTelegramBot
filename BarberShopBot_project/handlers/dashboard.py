from telegram import Update

from telegram.ext import CommandHandler, ContextTypes
from BarberShopBot_project.keyboards import remove_keyboard, web_app_inline_keyboard
from BarberShopBot_project.texts import WELCOME_BACK, USER_NOTIFICATION

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_BACK,
        reply_markup=web_app_inline_keyboard()
    )


def register_dashboard_handlers(app):
    app.add_handler(CommandHandler("menu", menu_command))
