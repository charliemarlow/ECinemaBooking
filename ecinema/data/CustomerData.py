from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class CustomerData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.get_user_info(key)

    def get_all_customers(self):
        return self.__db.execute(
            'SELECT * FROM customer'
        ).fetchall()

    def get_cards(self, key: str):
        return self.__db.execute(
            'SELECT * FROM credit_card WHERE cid = ?',
            (key,)
        ).fetchall()

    def get_promotion_users(self):
        return self.__db.execute(
            'SELECT * FROM customer WHERE subscribe_to_promo = 1'
        ).fetchall()

    def get_bookings(self, key):
        return self.__db.execute(
            'SELECT * FROM booking WHERE customer_id = ?',
            (key,)
        ).fetchall()

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

    def update_edit_info(self, data) -> str:
        self.__db.execute(
            'UPDATE customer SET customer_id = ?, first_name = ?, last_name = ?, '
            'username = ?, email = ?, phone_number = ?, '
            'address_id = ?, status = ? WHERE customer_id = ?',
            data
        )
        self.__db.commit()

    def get_user_info(self, user_id: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE username = ?', (user_id,)
        ).fetchone()

    def get_info_by_id(self, cust_id: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE customer_id = ?', (cust_id,)
        ).fetchone()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM customer WHERE customer_id = ?',
            (key,)
        )
        self.__db.commit()

    def delete_reviews(self, key: str):
        self.__db.execute(
            'DELETE FROM review WHERE customer_id = ?',
            (key,)
        )
        self.__db.commit()


    def get_info_by_email(self, email: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE email = ?', (email,)
        ).fetchone()
