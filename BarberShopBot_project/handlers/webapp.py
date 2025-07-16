import json
import logging
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from BarberShopBot_project.db import save_profile

# Настраиваем свой логгер
logger = logging.getLogger(__name__)

async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Всегда логируем заход в хэндлер
    logger.info("🔔 webapp_data_handler вызван")

    webapp = update.message.web_app_data
    if not webapp:
        logger.info("✖ Нет web_app_data в сообщении")
        return

    logger.info("ℹ Получены WebApp данные: %s", webapp.data)

    # Пытаемся распарсить JSON
    try:
        obj = json.loads(webapp.data)
    except json.JSONDecodeError:
        logger.error("❌ Ошибка разбора JSON: %s", webapp.data)
        return

    # Обрабатываем payload
    t = obj.get("type")
    if t == "profile_update":
        payload = obj.get("payload", {})
        logger.info("✅ profile_update, сохраняем: %s", payload)
        save_profile(
            telegram_id=update.effective_user.id,
            first_name = payload.get("first_name", ""),
            last_name  = payload.get("last_name", ""),
            patronymic = payload.get("patronymic", ""),
            phone      = payload.get("phone", ""),
            email      = payload.get("email", "")
        )
        await update.message.reply_text("✅ Профиль успешно сохранён!")
    else:
        logger.info("ℹ Неизвестный тип данных: %s", t)
        await update.message.reply_text(f"ℹ️ Неизвестный тип: {t}")

def register_webapp_handlers(app):
    app.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler),
        group=5
    )
