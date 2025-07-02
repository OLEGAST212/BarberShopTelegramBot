import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Логируем все необработанные исключения."""
    logger.error("Exception while handling update %s", update, exc_info=context.error)

def register_error_handler(app):
    app.add_error_handler(error_handler)
