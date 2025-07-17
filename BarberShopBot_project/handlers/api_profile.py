# handlers/api_profile.py

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from telegram import Bot
from init_data_py import InitData

from BarberShopBot_project.config import BOT_TOKEN
from BarberShopBot_project.db import get_profile, save_profile

router = APIRouter()


class ProfileIn(BaseModel):
    init_data: str
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str


class ProfileOut(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    email: str


def parse_and_validate(init_data: str) -> int:
    """
    Разбирает и проверяет подпись init_data через init-data-py.
    Возвращает telegram_id или кидает HTTPException(401).
    """
    try:
        init = InitData.parse(init_data)
        init.validate(bot_token=BOT_TOKEN, lifetime=3600 * 24)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid init_data: {e}")
    return init.user.id  # type: ignore


@router.get("/api/profile", response_model=ProfileOut)
async def api_get_profile(init_data: str = Query(..., alias="init_data")):
    user_id = parse_and_validate(init_data)
    return get_profile(user_id)


@router.post("/api/profile", response_model=ProfileOut)
async def api_write_profile(data: ProfileIn):
    user_id = parse_and_validate(data.init_data)

    # Сохраняем в БД
    save_profile(
        telegram_id=user_id,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic=data.patronymic,
        phone=data.phone,
        email=data.email,
    )

    # Уведомляем пользователя в чате
    Bot(token=BOT_TOKEN).send_message(
        chat_id=user_id,
        text="✅ Профиль успешно сохранён!"
    )

    # Возвращаем только что сохранённый профиль
    return get_profile(user_id)
