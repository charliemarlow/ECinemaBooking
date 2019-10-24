from abc import ABCMeta

class User(ABC):
    def __init__(self, userID, password):
        self.__userID = userID
        self.__password = password

    def getUserID(self):
        return self.__userID
]
    def setUserID(self, userID):
        self.__userID = userID
]
    def getPassword(self):
        return self.__password
]
    def setPassword(self, password):
        self.__password = password
    