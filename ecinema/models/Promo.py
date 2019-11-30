
from ecinema.models.model import Model
from ecinema.data.PromoData import PromoData

class Promo(Model):

    def __init__(self):
        self.__id = None

        self.__code = None
        self.__promo = None
        self.__promo_description = None
        self.__exp_date = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = PromoData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_promos(self):
        return self.__data_access.get_all_promos()


    def fetch_by_code(self, code: str):
        promo = self.__data_access.get_info_by_code(code)

        if promo is not None:
            self.set_id(promo['promo_id'])

            self.set_code(promo['code'])
            self.set_promo(promo['promo'])
            self.set_promo_description(promo['promo_description'])
            self.set_exp_date(promo['exp_date'])
            self.set_is_init()

            return True
        return False
    def fetch(self, key: str):
        promo = self.obj_as_dict(key)

        if promo is not None:
            self.set_id(promo['promo_id'])

            self.set_code(promo['code'])
            self.set_promo(promo['promo'])
            self.set_promo_description(promo['promo_description'])
            self.set_exp_date(promo['exp_date'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        promo = {}
        for key, value in kwargs.items():
            promo[key] = value


        self.set_code(promo['code'])
        self.set_promo(promo['promo'])
        self.set_promo_description(promo['promo_description'])
        self.set_exp_date(promo['exp_date'])
        self.set_is_init()

        member_tup = (self.get_code(), self.get_promo(), self.get_promo_description(), self.get_exp_date())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (self.get_code(), self.get_promo(), self.get_promo_description(), self.get_exp_date(), self.get_id())

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

    def get_promo_description(self) -> str:
        return self.__promo_description

    def set_promo_description(self, promo_description: str):
        self.__promo_description = promo_description

    def get_exp_date(self) -> str:
        return self.__exp_date

    def set_exp_date(self, exp_date: str):
        self.__exp_date = exp_date

