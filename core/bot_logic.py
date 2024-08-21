from aiogram import Bot, Dispatcher, F
import asyncio
import logging
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from basic import get_start, help_message, get_hello, users_info, forget_user
from keyboard.callback import select_magnitude
from keyboard.callbackdata import Magnitude
from settings import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from get_news import get_news
from commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.admin_id, text="Бот запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(settings.admin_id, text="Бот остановлен")


async def start():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(get_news, trigger='interval', seconds=300, kwargs={'bot': bot})
    scheduler.start()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_start, F.text == "/start")
    dp.callback_query.register(select_magnitude, Magnitude.filter())
    dp.message.register(help_message, F.text == "/help")
    dp.message.register(forget_user, F.text == "/forget")
    dp.message.register(get_hello, F.text.lower().startswith("привет"))
    dp.message.register(users_info, F.text == "users")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
