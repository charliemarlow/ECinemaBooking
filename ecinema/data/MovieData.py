from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class MovieData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM movie WHERE movie_id = ?',
            (key,)
        ).fetchone()

    def get_all_movies(self):
        return self.__db.execute(
            'SELECT * FROM movie'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM movie WHERE movie_id = ?',
            key
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO movie '
            '(title, category, director, producer, synopsis, '
            'picture, video, duration_as_minutes, rating) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE movie SET title = ?, category = ?, '
            'director = ?, producer = ?, synopsis = ?, '
            'picture = ?, video = ?, duration_as_minutes = ?, '
            'rating = ? '
            'WHERE movie_id = ?',
            data
        )

        self.__db.commit()
