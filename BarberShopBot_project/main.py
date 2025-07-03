import logging
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
import db
from handlers import (
    register_auth_handlers,
    register_dashboard_handlers,
    register_echo_handlers,
    register_error_handler,
    register_admin_handlers
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    db.init_db()
    db.init_appointments_table()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем все группы хэндлеров
    register_auth_handlers(app)
    register_dashboard_handlers(app)
    register_admin_handlers(app)   # ← сначала админ-хэндлер
    register_echo_handlers(app)
    register_error_handler(app)

    logger.info("Bot is starting…")

    app.run_polling()

if __name__ == "__main__":
    main()
