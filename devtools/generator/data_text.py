


body = '''
from ecinema.data.access import DataAccess
from ecinema.data.db import get_db

class {capital_name}Data(DataAccess):

    def __init__(self):
        self.__db = get_db()

    def get_info(self, key: str):
        return self.__db.execute(
            'SELECT * FROM {table} WHERE {table_id} = ?',
            (key,)
        ).fetchone()

    def get_all_{table}(self):
        return self.__db.execute(
            'SELECT * FROM {table}'
        ).fetchall()

    def delete(self, key: str):
        self.__db.execute(
            'DELETE FROM {table} WHERE {table_id} = ?',
            key
        )
        self.__db.commit()

    def insert_info(self, data) -> str:
        cursor = self.__db.cursor()
        cursor.execute(
            'INSERT INTO {table} '
            '({attr}) '
            'VALUES ({values})',
            data
        )

        row_id = cursor.lastrowid
        self.__db.commit()
        return row_id

    def update_info(self, data) -> str:
        self.__db.execute(
            'UPDATE {table} SET {update}'
            'WHERE {table_id} = ?',
            data
        )

        self.__db.commit()
'''
