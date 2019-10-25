import re
from werkzeug.security import check_password_hash


class User:
    def __init__(self):
        self.__username = None
        self.__password = None

    def get_username(self) -> str:
        return self.__username

    def set_username(self, user: str):
        self.__username = user

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password: str):
        self.__password = password
