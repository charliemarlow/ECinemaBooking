from ecinema.models.model import Model
from ecinema.data.AddressData import AddressData


class Address(Model):

    def __init__(self):
        self.__id = None
        self.__street = None
        self.__city = None
        self.__state = None
        self.__zip = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = AddressData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def fetch(self, key: str):
        addr = self.obj_as_dict(key)
        if addr is not None:
            self.set_id(addr['address_id'])
            self.set_street(addr['street'])
            self.set_city(addr['city'])
            self.set_state(addr['state'])
            self.set_zip(addr['zip_code'])
            self.set_is_init()
            return True

        return False

    def create(self, **kwargs):
        addr = {}
        for key, value in kwargs.items():
            addr[key] = value

        self.set_street(addr['street'])
        self.set_city(addr['city'])
        self.set_state(addr['state'])
        self.set_zip(addr['zip_code'])
        self.set_is_init()

        member_tup = (self.get_street(),
                      self.get_city(),
                      self.get_state(),
                      self.get_zip())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> str:
        if not self.is_initialized():
            return False

        member_tup = (self.get_street(),
                      self.get_city(), self.get_state(),
                      self.get_zip(), self.get_id())
        print(member_tup)
        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_id(self) -> str:
        return self.__id

    def set_id(self, addr_id: str):
        self.__id = addr_id

    def get_street(self) -> str:
        return self.__street

    def set_street(self, street: str):
        self.__street = street

    def get_city(self) -> str:
        return self.__city

    def set_city(self, city: str):
        self.__city = city

    def get_state(self) -> str:
        return self.__state

    def set_state(self, state: str):
        self.__state = state

    def get_zip(self) -> str:
        return self.__zip

    def set_zip(self, zip_code: str):
        self.__zip = zip_code
