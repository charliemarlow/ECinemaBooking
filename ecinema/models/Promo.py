
from ecinema.models.model import Model
from ecinema.data.PromoData import PromoData

class Promo(Model):

    def __init__(self):
        self.__id = None

        self.__code = None
        self.__promo = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = PromoData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_promos(self):
        return self.__data_access.get_all_promos()

    def fetch(self, key: str):
        promo = self.obj_as_dict(key)

        if promo is not None:
            self.set_id(promo['promo_id'])

            self.set_code(promo['code'])
            self.set_promo(promo['promo'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        promo = {}
        for key, value in kwargs.items():
            promo[key] = value


        self.set_code(promo['code'])
        self.set_promo(promo['promo'])
        self.set_is_init()

        member_tup = (self.get_code(), self.get_promo())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (self.get_code(), self.get_promo(), self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)


    def get_code(self) -> str:
        return self.__code

    def set_code(self, code: str):
        self.__code = code

    def get_promo(self) -> str:
        return self.__promo

    def set_promo(self, promo: str):
        self.__promo = promo

