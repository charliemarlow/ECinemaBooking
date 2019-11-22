
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class ReviewData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM review WHERE review_id = ?',
            (key,)
        ).fetchone()

    def get_all_reviews_by_movie(self, mid):
        return self.__db.execute(
            'SELECT * FROM review WHERE movie_id = ?',
            mid
        ).fetchall()

    def get_name(self, cid):
        name =  self.__db.execute(
            'SELECT first_name, last_name FROM customer WHERE customer_id = ?',
            (cid,)
        ).fetchone()
        return name['first_name'], name['last_name']

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM review WHERE review_id = ?',
            (key,)
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        print(data)
        cursor.execute(
            'INSERT INTO review '
            '(customer_id, movie_id, rating, subject, review) '
            'VALUES (?, ?, ?, ?, ?)',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE review SET customer_id = ?, movie_id = ?, rating = ?, subject = ?, review = ?'
            'WHERE review_id = ?',
            data
        )

        self.__db.commit()
