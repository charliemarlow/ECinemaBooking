import abc


class DataAccess(abc.ABC):
    @abc.abstractmethod
    def get_info(self, key: str):
        pass

    @abc.abstractmethod
    def insert_info(self, data) -> str:
        pass

    @abc.abstractmethod
    def update_info(self, data) -> str:
        pass
