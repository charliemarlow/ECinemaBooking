from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class AddressData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM address WHERE address_id = ?',
            (key,)
        ).fetchone()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO address '
            '(street, city, state, zip_code) '
            'VALUES (?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def delete(self, key):
        # if it has a customer, set that address_id to NULL
        has_customer = self.__db.execute(
            'SELECT * FROM customer WHERE address_id = ?',
            (key,)
        ).fetchone() is not None
        if has_customer:
            self.__db.execute(
                'UPDATE customer SET address_id = null WHERE address_id = ?',
                (key,)
            )
            self.__db.commit()

        # if it has a credit card, do NOT delete
        # but it's good to go ahead and unlink it from the customer
        has_card = self.__db.execute(
            'SELECT * FROM credit_card WHERE aid = ?',
            (key,)
        ).fetchone() is not None

        if not has_card:
            self.__db.execute(
                'DELETE FROM address WHERE address_id = ?',
                (key,)
            )
            self.__db.commit()

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE address SET street = ?, '
            'city = ?, state = ?, zip_code = ?'
            'WHERE address_id = ?',
            data
        )
        self.__db.commit()

    def get_address_info(self, cust_id: str):
        return self.get_info(cust_id)
