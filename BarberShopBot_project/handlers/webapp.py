import json
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from BarberShopBot_project.db import save_profile

async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Telegram.WebApp.sendData придёт в update.message.web_app_data
    w = update.message.web_app_data
    if not w:
        return

    try:
        obj = json.loads(w.data)
    except json.JSONDecodeError:
        await update.message.reply_text("❌ Неверный формат данных.")
        return

    if obj.get("type") == "profile_update":
        p = obj["payload"]
        save_profile(
            telegram_id=update.effective_user.id,
            first_name=p.get("first_name", ""),
            last_name=p.get("last_name", ""),
            patronymic=p.get("patronymic", ""),
            phone=p.get("phone", ""),
            email=p.get("email", "")
        )
        await update.message.reply_text("✅ Профиль сохранён!")
    else:
        await update.message.reply_text("ℹ️ Получены неизвестные данные.")

def register_webapp_handlers(app):
    app.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler),
        group=5
    )
