# пример на FastAPI: web_api.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from BarberShopBot_project.db import get_profile, save_profile
from telegram import Bot
from BarberShopBot_project.config import BOT_TOKEN
import hmac, hashlib

app = FastAPI()
bot = Bot(token=BOT_TOKEN)

def verify_init_data(init_data: str) -> int:
    # Валидируем подпись initData → возвращаем telegram_id
    ...

@app.get("/api/profile")
async def read_profile(init_data: str):
    user_id = verify_init_data(init_data)
    return get_profile(user_id)

class ProfileIn(BaseModel):
    init_data: str
    first_name: str
    last_name:  str
    patronymic: str
    phone:      str
    email:      str

@app.post("/api/profile")
async def write_profile(data: ProfileIn):
    user_id = verify_init_data(data.init_data)
    save_profile(user_id, data.first_name, data.last_name, data.patronymic, data.phone, data.email)
    bot.send_message(user_id, "✅ Профиль сохранён!")
    return {"ok": True}
