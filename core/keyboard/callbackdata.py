from aiogram.filters.callback_data import CallbackData


class Magnitude(CallbackData, prefix='magnitude'):
    magnitude: int
