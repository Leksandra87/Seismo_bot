from aiogram import Bot
from pars_logic import collect_news
import json
from settings import settings
from datetime import datetime
from db_logic import from_db
from pytz import timezone


async def get_news(bot: Bot):
    collect_news()
    with open(f'{settings.base_dir}/saves/fresh.json', "r", encoding="utf-8") as file:
        news = json.load(file)
    users_list = from_db()
    if news:
        for user in users_list:
            for time, data in news.items():
                date_time = datetime.fromtimestamp(int(time)).astimezone(timezone('Europe/Moscow')).strftime(
                    "%d-%m-%Y (%H:%M)")
                magnitude = data['magnitude']
                depth = data['depth']
                location = data['location']
                result_data = f'<b>{date_time}</b> произошло землетрясение магнитудой:\n ' \
                              f'<b>{magnitude} баллов</b>, на глубине: {depth} км,\n <b>{location}</b>'
                if magnitude < user['magnitude']:
                    continue
                else:
                    await bot.send_message(str(user['id']), result_data)
