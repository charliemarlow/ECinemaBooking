from ecinema.data.access import DataAccess
from ecinema.data.db import get_db


class AdminData(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM admin WHERE username = ?',
            (key,)
        ).fetchone()

    def get_all_admins(self):
        return self.__db.execute(
            'SELECT * FROM admin'
        ).fetchall()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO admin (username, password) '
            'VALUES (?, ?)',
            data
        )
        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE admin SET username = ?, password = ? '
            'WHERE username = ?',
            data
        )
        self.__db.commit()

    def delete(self, aid):
        self.__db.execute(
            'DELETE FROM admin WHERE admin_id = ?',
            (aid,)
        )
        self.__db.commit()

    def is_unique_name(self, username):
        unique_admin = self.__db.execute(
            'SELECT * FROM admin WHERE username = ?',
            (username,)
        ).fetchone() is None

        unique_customer = self.__db.execute(
            'SELECT * FROM customer WHERE username = ?',
            (username,)
        ).fetchone() is None

        unique_email = self.__db.execute(
            'SELECT * FROM customer WHERE email = ?',
            (username,)
        ).fetchone() is None

        return (unique_admin and
                unique_customer and
                unique_email)
