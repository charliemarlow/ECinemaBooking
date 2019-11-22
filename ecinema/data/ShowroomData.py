from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class ShowroomData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM showroom WHERE showroom_id = ?',
            (key,)
        ).fetchone()

    def get_all_showrooms(self):
        return self.__db.execute(
            'SELECT * FROM showroom'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM showroom WHERE showroom_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO showroom '
            '(theater_id, num_seats, showroom_name) '
            'VALUES (?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE showroom SET theater_id = ?, num_seats = ?, showroom_name = ?'
            'WHERE showroom_id = ?',
            data
        )

        self.__db.commit()

    def unique_name(self, name) -> bool:
        return self.__db.execute(
            'SELECT * FROM showroom WHERE showroom_name = ?',
            (name,)
        ).fetchone() is None

    def get_all_showtimes(self, key: str):
        return self.__db.execute(
            'SELECT * FROM showtime WHERE showroom_id = ?',
            (key,)
        ).fetchall()

    def validate_seats(self, key: str, num_seats: int) -> bool:
        return self.__db.execute(
            'SELECT * FROM showtime WHERE showroom_id = ? AND (available_seats - ?) > 0',
            (key, num_seats)
        ).fetchone() is not None

    def update_seat_number(self, num, sid):
        self.__db.execute(
            'UPDATE showtime SET available_seats = (available_seats + ?) WHERE showroom_id = ?',
            (num, sid)
        )
        self.__db.commit()

    def check_valid_decrease(self, num, sid):
        return self.__db.execute('SELECT * FROM showtime WHERE showroom_id = ? AND (available_seats + ? ) < 0', (sid, num)).fetchone() is None
