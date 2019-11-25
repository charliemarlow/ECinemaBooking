
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class ShowtimeData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM showtime WHERE showtime_id = ?',
            (key,)
        ).fetchone()

    def get_all_showtimes(self):
        return self.__db.execute(
            'SELECT * FROM showtime'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM showtime WHERE showtime_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO showtime '
            '(time, available_seats, movie_id, showroom_id) '
            'VALUES (?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE showtime SET time = ?, available_seats = ?, movie_id = ?, showroom_id = ?'
            'WHERE showtime_id = ?',
            data
        )

        self.__db.commit()

    def get_tickets(self, sid):
        return self.__db.execute(
            'SELECT * FROM ticket WHERE showtime_id = ?',
            (sid,)
        ).fetchall()
