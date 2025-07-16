import logging
from BarberShopBot_project.db import init_db
from handlers.webapp import register_webapp_handlers
from telegram import MenuButtonWebApp, WebAppInfo
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN, WEB_APP_URL

from handlers import (
    register_auth_handlers,
    register_dashboard_handlers,
    register_echo_handlers,
    register_error_handler,
    register_admin_handlers
)
from telegram.ext import MessageHandler, filters

async def debug_all(update, context):
    print(">> Любое update пришло:", update)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# async def on_startup(app):
#     # Заменяем кнопку меню (⋮ → Открыть мини-приложение) на ваш текст и URL
#     await app.bot.set_chat_menu_button(
#         menu_button=MenuButtonWebApp(
#             text="ОНЛАЙН - ЗАПИСЬ",
#             web_app=WebAppInfo(url=WEB_APP_URL)
#         )
#     )
#     logger.info("Chat menu button updated to WebApp")

def main():
    init_db()
    builder = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        # .post_init(on_startup)
    )
    app = builder.build()

    # 2) Регистрируйте все ваши хэндлеры
    register_auth_handlers(app)
    register_dashboard_handlers(app)
    register_admin_handlers(app)
    register_echo_handlers(app)
    register_error_handler(app)
    register_webapp_handlers(app)
    app.add_handler(MessageHandler(filters.ALL, debug_all), group=10)
    logger.info("Bot is starting…")
    app.run_polling()



if __name__ == "__main__":
    main()
