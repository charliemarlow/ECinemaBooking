
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class PriceData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM price WHERE price_id = ?',
            (key,)
        ).fetchone()

    def get_all_prices(self):
        return self.__db.execute(
            'SELECT * FROM price'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM price WHERE price_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO price '
            '(price) '
            'VALUES (?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE price SET price = ?'
            'WHERE price_id = ?',
            data
        )

        self.__db.commit()

    def get_tax(self):
        return self.__db.execute(
        'SELECT * FROM price WHERE price_id = "tax"'
        ).fetchone()

    def get_fee(self):
        return self.__db.execute(
        'SELECT * FROM price WHERE price_id = "fees"'
        ).fetchone()
