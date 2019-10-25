import abc


class Model(abc.ABC):

    def __init__(self):
        self.__id = None
        self.__data_access = None
        self.__is_init = False

    @abc.abstractmethod
    def fetch(self, key: str):
        # loads model from DB
        pass

    @abc.abstractmethod
    def create(self, *args):
        pass

    @abc.abstractmethod
    def save(self) -> bool:
        pass

    @abc.abstractmethod
    def obj_as_dict(self, key: str):
        pass

    def set_id(self, primary_id: str):
        self.__id = primary_id

    def get_id(self) -> str:
        return self.__id

    def is_initialized(self) -> bool:
        return self.__is_init

    def set_is_init(self):
        self.__is_init = True
