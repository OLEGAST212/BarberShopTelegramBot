import logging
import hmac
import hashlib
import json
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from telegram import Bot, MenuButtonDefault
from telegram.ext import ApplicationBuilder

from config import BOT_TOKEN, WEB_APP_URL
from BarberShopBot_project.db import init_db, get_profile, save_profile
from handlers.auth import register_auth_handlers
from handlers.dashboard import register_dashboard_handlers
from handlers.admin import register_admin_handlers
from handlers.echo import register_echo_handlers
from handlers.webapp import register_webapp_handlers
from handlers.errors import register_error_handler

# — API + статика —
api = FastAPI()
bot = Bot(token=BOT_TOKEN)

# монтируем собранный фронт из папки static/
api.mount("/", StaticFiles(directory="static", html=True), name="static")

class ProfileIn(BaseModel):
    init_data: str
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str

def verify_init_data(init_data: str) -> int:
    try:
        data = dict(pair.split("=", 1) for pair in init_data.split("&"))
    except Exception:
        raise HTTPException(400, "Invalid init_data format")
    hash_received = data.pop("hash", None)
    if not hash_received:
        raise HTTPException(400, "No hash in init_data")
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    computed = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed, hash_received):
        raise HTTPException(400, "Invalid init_data signature")
    user_json = data.get("user")
    if not user_json:
        raise HTTPException(400, "No user in init_data")
    try:
        user = json.loads(user_json)
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid user JSON")
    user_id = user.get("id")
    if not isinstance(user_id, int):
        raise HTTPException(400, "Invalid user id")
    return user_id

@api.get("/api/profile")
async def read_profile(init_data: str):
    user_id = verify_init_data(init_data)
    return get_profile(user_id)

@api.post("/api/profile")
async def write_profile(data: ProfileIn):
    user_id = verify_init_data(data.init_data)
    save_profile(
        telegram_id=user_id,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic=data.patronymic,
        phone=data.phone,
        email=data.email
    )
    bot.send_message(chat_id=user_id, text="✅ Профиль успешно сохранён!")
    return {"ok": True}

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="info")

# — Telegram‑бот —
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_startup(app):
    await app.bot.set_chat_menu_button(menu_button=MenuButtonDefault())
    logger.info("Chat menu button reset to default")

def main():
    init_db()
    proc = Process(target=run_api, daemon=True)
    proc.start()
    logger.info("Web API запущен (PID=%s)", proc.pid)

    builder = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup)
    app = builder.build()

    register_auth_handlers(app)
    register_dashboard_handlers(app)
    register_admin_handlers(app)
    register_echo_handlers(app)
    register_error_handler(app)
    register_webapp_handlers(app)

    logger.info("Телеграм‑бот стартует…")
    app.run_polling()

if __name__ == "__main__":
    main()
