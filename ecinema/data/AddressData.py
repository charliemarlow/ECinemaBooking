from ecinema.data.db import get_db


class AddressData:

    def __init__(self):
        self.__db = get_db()

    def get_address_info(self, cust_id: str):
        addr = self.__db.execute(
            'SELECT * FROM address WHERE cid = ?',
            (cust_id,)
        ).fetchone()

        return addr

    def set_street(self, cid: str, street: str):
        self.__db.execute(
            'UPDATE address SET street = ? WHERE cid = ?',
            (street, cid)
        )
        self.__db.commit()

    def set_city(self, cid: str, city: str):
        self.__db.execute(
            'UPDATE address SET city = ? WHERE cid = ?',
            (city, cid)
        )
        self.__db.commit()

    def set_state(self, cid: str, state: str):
        self.__db.execute(
            'UPDATE address SET state = ? WHERE cid = ?',
            (state, cid)
        )
        self.__db.commit()

    def set_zip_code(self, cid: str, zip_code: str):
        self.__db.execute(
            'UPDATE address SET zip_code = ? WHERE cid = ?',
            (zip_code, cid)
        )
        self.__db.commit()
