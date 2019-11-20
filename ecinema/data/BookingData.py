
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class BookingData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM booking WHERE booking_id = ?',
            (key,)
        ).fetchone()

    def get_all_bookings(self):
        return self.__db.execute(
            'SELECT * FROM booking'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM booking WHERE booking_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO booking '
            '(order_id, total_price, credit_card_id, promo_id, movie_id, customer_id, showtime_id, order_date) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE booking SET order_id = ?, total_price = ?, credit_card_id = ?, promo_id = ?, movie_id = ?, customer_id = ?, showtime_id = ?, order_date = ?'
            'WHERE booking_id = ?',
            data
        )

        self.__db.commit()

    def get_tickets(self, bid) -> str:
        return self.__db.execute(
            'SELECT * FROM ticket WHERE booking_id = ?',
            (bid,)
        ).fetchall()
