import json
from os import path
import requests
from bs4 import BeautifulSoup
from geopy import Yandex, point
from settings import settings


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
}
URL = "https://voshod-solnca.ru/earthquake/"


def get_location(lat: str, lon: str) -> str:
    """
    Определение места по координатам
    """
    dot = point.Point(float(lat), float(lon))
    location = Yandex(api_key=settings.api_key, domain='geocode-maps.yandex.ru').reverse(dot,
                                                                                         exactly_one=True,
                                                                                         kind='locality',
                                                                                         lang='ru_RU')
    if location is None:
        location = f"Координаты: {lat}, {lon}"
    return location


def collect_news():
    """
    Получает с сайта информацию о последних 10 сейсмотолчках, записывает данные в json-файл
    """
    check = path.exists(f'{settings.base_dir}/saves/info_dict.json')
    if check:
        with open(f'{settings.base_dir}/saves/info_dict.json', "r", encoding="utf-8") as file:
            previous_news = json.load(file)
            fresh = {}
    headers = HEADERS
    url = URL
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    lines = soup.find('div', class_='earthquake-table block').find('tbody').find_all('tr')
    info = {}

    for val in lines[::-1]:
        data = val.find_all('td')
        timestamp = data[0].get('data-timestamp')
        magnitude = round(float(data[3].get('data-magnitude')), 2)
        depth = round(float(data[4].get('data-depth')), 2)
        lat = data[5].get('data-lat')  # str
        lon = data[6].get('data-lon')  # str
        location = str(get_location(lat, lon))

        info[timestamp] = {
            'magnitude': magnitude,
            'depth': depth,
            'location': location,
        }

        if check:
            if timestamp not in previous_news:
                fresh[timestamp] = {
                    'magnitude': magnitude,
                    'depth': depth,
                    'location': location,
                }

    with open(f'{settings.base_dir}/saves/info_dict.json', "w", encoding="utf-8") as file:
        json.dump(info, file, indent=4, ensure_ascii=False)

    if check:
        with open(f'{settings.base_dir}/saves/fresh.json', "w", encoding="utf-8") as file:
            json.dump(fresh, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    collect_news()
