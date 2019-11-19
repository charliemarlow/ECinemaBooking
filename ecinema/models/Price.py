
from ecinema.models.model import Model
from ecinema.data.PriceData import PriceData

class Price(Model):

    def __init__(self):
        self.__id = None

        self.__price = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = PriceData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_prices(self):
        return self.__data_access.get_all_prices()

    def fetch(self, key: str):
        price = self.obj_as_dict(key)

        if price is not None:
            self.set_id(price['price_id'])

            self.set_price(price['price'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        price = {}
        for key, value in kwargs.items():
            price[key] = value


        self.set_price(price['price'])
        self.set_is_init()

        member_tup = (self.get_price())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (self.get_price(), self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)


    def get_price(self) -> str:
        return self.__price

    def set_price(self, price: str):
        self.__price = price

    def get_tax_price(self):
        tax = self.__data_access.get_tax()
        return float(tax['price'])

    def get_online_fee(self):
        fee = self.__data_access.get_fee()
        return float(fee['price'])
