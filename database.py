import sqlite3

from parser import FoundedObject

timeout = 3000

create_table_command = '''CREATE TABLE IF NOT EXISTS 
                            favourites(
                                        id INTEGER PRIMARY KEY, 
                                        user_id INTEGER, 
                                        title_name TEXT, 
                                        original_name TEXT,
                                        rating TEXT,
                                        image TEXT,
                                        url TEXT,
                                        type TEXT) '''


class Database:
    def __init__(self):
        with sqlite3.connect('favourites.db') as db:
            cur = db.cursor()
            cur.execute(create_table_command)

    @staticmethod
    def get_user_favourites(user_id: int) -> list[FoundedObject]:
        with sqlite3.connect('favourites.db', timeout=timeout) as db:
            cur = db.cursor()
            cur.execute(f'SELECT * FROM favourites WHERE user_id = {user_id}')
            t = cur.fetchall()

        result = []

        for i in t:
            result.append(
                FoundedObject(name=i[2], original_name=i[3], rating=i[4], image_url=i[5], url=i[6], title_type=i[7]))

        return result

    @staticmethod
    def add_favourites(user_id: int, title: FoundedObject):
        with sqlite3.connect('favourites.db', timeout=timeout) as db:
            cur = db.cursor()
            c = f'SELECT * FROM favourites WHERE user_id = {user_id} AND url = "{title.url}"'
            print(c)
            cur.execute(c)
            if len(cur.fetchall()) == 0:
                cur.execute(
                    f'INSERT INTO favourites(user_id, title_name, original_name, rating, image, url, type) VALUES({user_id}, "{title.name}", "{title.original_name}", "{title.rating}", "{title.image_url}", "{title.url}", "{title.type}")')

    @staticmethod
    def delete_favourite(user_id: int, title_url: str):
        with sqlite3.connect('favourites.db', timeout=timeout) as db:
            cur = db.cursor()
            cur.execute(f'SELECT * FROM favourites WHERE user_id = {user_id} AND url = "{title_url}"')
            if len(cur.fetchall()) != 0:
                cur.execute(f'DELETE FROM favourites WHERE user_id = {user_id} AND url = "{title_url}"')
