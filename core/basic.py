from aiogram import Bot
from aiogram.types import Message
from keyboard.selection import get_keyboard
from settings import settings
from db_logic import from_db, del_user


async def get_hello(message: Message, bot: Bot):
    await message.answer(f"И тебе привет, {message.from_user.first_name}!")


async def get_start(message: Message, bot: Bot):
    await message.answer(f"Выберите магнитуду", reply_markup=get_keyboard())


async def help_message(message: Message, bot: Bot):
    await message.answer(
        "Это бот собирает информацию о землетрясениях с сайта <b>https://voshod-solnca.ru/earthquake/</b>. "
        "Для начала работы нажмите кнопку <b>/start</b> в меню бота и выберите желаемую магнитуду")


async def users_info(message: Message, bot: Bot):
    """
    Показывает информацию о пользователях - id  и выбранную магнитуду
    """
    if str(message.from_user.id) == settings.admin_id:
        users_list = from_db()
        data = [f"{user['id']} - {user['magnitude']}" for user in users_list]
        text = '\n'.join(data)
        await message.answer(text)
    else:
        await message.answer("Информация доступна только администратору")


async def forget_user(message: Message, bot: Bot):
    """
    Удаляет пользователя из списка рассылки
    """
    del_user(message.from_user.id)
    await message.answer("Вы больше не будете получать сообщения от этого бота.\n"
                         " Для возобновления рассылки нажмите <b>/start</b> и выберите магнитуду")
