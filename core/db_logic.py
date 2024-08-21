import sqlite3
from settings import settings


def check_db_exist(cursor):
    query = """CREATE TABLE IF NOT EXISTS Users(id INTEGER, magnitude INTEGER)"""
    cursor.execute(query)


def check_user(cursor, id):
    cursor.execute('SELECT id FROM Users WHERE id = ?', (id,))
    result = cursor.fetchall()
    return result


def db_logic(id: int, magnitude: int) -> None:
    with sqlite3.connect(f'{settings.base_dir}/saves/users.db') as db:
        cursor = db.cursor()
        check_db_exist(cursor)
        if check_user(cursor, id):
            cursor.execute('UPDATE Users SET magnitude = ? WHERE id = ?', (magnitude, id))
        else:
            cursor.execute('INSERT INTO Users (id, magnitude) VALUES (?, ?)',
                           (id, magnitude))


def from_db() -> list:
    with sqlite3.connect(f'{settings.base_dir}/saves/users.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Users')
        all_users = cursor.fetchall()
        users_list = []
        for user in all_users:
            user_dict = {
                'id': user[0],
                'magnitude': user[1]
            }
            users_list.append(user_dict)
    return users_list


def del_user(id: int) -> None:
    """
    Удаление записи из БД по id пользователя
    """
    with sqlite3.connect(f'{settings.base_dir}/saves/users.db') as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM Users WHERE id = ?', (id,))
