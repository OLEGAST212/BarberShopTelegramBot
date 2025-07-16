
import json
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from BarberShopBot_project.db import save_profile

async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_str = update.message.web_app_data.data
    data = json.loads(data_str)
    if data.get("type") == "profile_update":
        p = data["payload"]
        save_profile(
            telegram_id=update.effective_user.id,
            first_name=p.get("first_name",""),
            last_name=p.get("last_name",""),
            patronymic=p.get("patronymic",""),
            phone=p.get("phone",""),
            email=p.get("email","")
        )
        await update.message.reply_text("✅ Профиль успешно сохранён!")
