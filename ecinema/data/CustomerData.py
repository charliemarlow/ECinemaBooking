from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class CustomerData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.get_user_info(key)

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO customer (first_name, last_name, '
            'email, subscribe_to_promo, phone_number, username, password, status) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            data
        )
        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE customer SET first_name = ?, last_name = ?, '
            'email = ?, subscribe_to_promo = ?, username = ?, '
            'password = ?, phone_number = ?, status = ?, address_id = ? WHERE customer_id = ?',
            data
        )
        self.__db.commit()

    def get_user_info(self, user_id: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE username = ?', (user_id,)
        ).fetchone()

    def get_info_by_email(self, email: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE email = ?', (email,)
        ).fetchone()
