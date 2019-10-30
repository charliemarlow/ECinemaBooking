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
