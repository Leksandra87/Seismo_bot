from aiogram import Bot
from aiogram.types import CallbackQuery
from .callbackdata import Magnitude
from core.db_logic import db_logic


async def select_magnitude(call: CallbackQuery, bot: Bot, callback_data: Magnitude):
    magnitude = callback_data.magnitude
    data = f"{call.from_user.first_name}, вам будут поступать сообщения о землетрясениях магнитудой {magnitude} и более баллов"
    db_logic(call.from_user.id, magnitude)
    await call.message.answer(data)
    await call.answer()
