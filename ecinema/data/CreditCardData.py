from ecinema.data.access import DataAccess
from ecinema.data.db import get_db
from ecinema.models.Address import Address
from datetime import datetime


class CreditCardData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM credit_card WHERE credit_card_id = ?',
            (key,)
        ).fetchone()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM credit_card WHERE credit_card_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO credit_card '
            '(cid, aid, card_number, last_four, cvv, '
            'exp_date, type) '
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE credit_card SET cid = ?, aid = ?, '
            'card_number = ?, last_four = ?, cvv = ?, '
            'exp_date = ?, type = ?'
            'WHERE credit_card_id = ?',
            data
        )
        self.__db.commit()

    def get_credit_card_info(self, cust_id: str):
        return self.get_info(cust_id)
