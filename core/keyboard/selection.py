from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callbackdata import Magnitude


def get_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    for val in range(6):
        keyboard_builder.button(text=f'{val} и более', callback_data=Magnitude(magnitude=val))
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()
