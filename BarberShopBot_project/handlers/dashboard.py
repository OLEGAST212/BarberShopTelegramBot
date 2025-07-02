from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from BarberShopBot_project.keyboards import remove_keyboard
from BarberShopBot_project.texts import WELCOME_BACK

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu — показать личный кабинет."""
    await update.message.reply_text(WELCOME_BACK, reply_markup=remove_keyboard())

def register_dashboard_handlers(app):
    app.add_handler(CommandHandler("menu", menu_handler))
