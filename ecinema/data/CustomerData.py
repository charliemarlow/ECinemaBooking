from ecinema.data.db import get_db


class CustomerData:

    def __init__(self):
        self.__db = get_db()


    def get_user_info(self, user_id: str):
        return self.__db.execute(
            'SELECT * FROM customer WHERE username = ?', (user_id,)
        ).fetchone()

    def set_first_name(self, cid: str, first: str):
        self.__db.execute(
            'UPDATE customer SET first_name = ? WHERE customer_id = ?',
            (first, cid)
        )
        self.__db.commit()


    def set_last_name(self, cid: str, last: str):
        self.__db.execute(
            'UPDATE customer SET last_name = ? WHERE customer_id = ?',
            (last, cid)
        )
        self.__db.commit()


    def set_email(self, cid: str, email: str):
        self.__db.execute(
            'UPDATE customer SET email = ? WHERE customer_id = ?',
            (email, cid)
        )
        self.__db.commit()
