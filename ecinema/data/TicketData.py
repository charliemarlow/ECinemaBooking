
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class TicketData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM ticket WHERE ticket_id = ?',
            (key,)
        ).fetchone()

    def get_all_tickets(self):
        return self.__db.execute(
            'SELECT * FROM ticket'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM ticket WHERE ticket_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO ticket '
            '(showtime_id, booking_id, age, seat_number) '
            'VALUES (?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE ticket SET showtime_id = ?, booking_id = ?, age = ?, seat_number = ?'
            'WHERE ticket_id = ?',
            data
        )

        self.__db.commit()
