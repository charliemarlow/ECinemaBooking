from abc import ABCMeta

class User(ABC):
    def __init__(self, userID, password):
        self.__userID = userID
        self.__password = password

    def get_user_id(self):
        return self.__userID

    def set_user_id(self, userID):
        self.__userID = userID

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password
