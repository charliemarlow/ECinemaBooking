
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class PromoData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM promo WHERE promo_id = ?',
            (key,)
        ).fetchone()

    def get_all_promos(self):
        return self.__db.execute(
            'SELECT * FROM promo'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM promo WHERE promo_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO promo '
            '(code, promo) '
            'VALUES (?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE promo SET code = ?, promo = ?'
            'WHERE promo_id = ?',
            data
        )

        self.__db.commit()
