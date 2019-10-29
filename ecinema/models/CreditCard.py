from ecinema.models.model import Model
from ecinema.data.CreditCardData import CreditCard
from ecinema.models.Address import Address
from datetime import datetime

class CreditCard(Model):

    def _init__(self):
        self.__id = None
        self.__cc_number = None
        self.__cvv = None
        self.__expiration_date = None
        self.__billing_address = None
        self.__is_init = False
        self.__data_access = CreditCardData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def fetch(self, key: str):
        card = self.obj_as_dict(key))
        if card is not None:
            self.set_id(card['card_id'])
            self.set_cc_number(card['cc_number'])
            self.set_cvv(card['cvv'])
            self.set_expiration_date(card['expiration_date'])
            self.set_billing_address(card['billing_address'])
            self.set_is_init()
            return True

        return False
    
    def create(self, **kwargs):
        card = {}
        for key, value in kwargs.items():
            card[key] = value


        self.set_id(card['card_id'])
        self.set_cc_number(card['cc_number'])
        self.set_cvv(card['cvv'])
        self.set_expiration_date(card['expiration_date'])
        self.set_billing_address(card['billing_address'])
        self.set_is_init()

        member_tup = (self.get_cc_number(),
                      self.get_cvv(),
                      self.get_expiration_date(),
                      self.get_billing_address())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> str:
        if not self.is_initialized():
            return False

        member_tup = (self.get_cc_number(),
                       self.get_cvv(), self.get_expiration_date(),
                       self.get_billing_address(), self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def get_id(self) -> str:
        return self.__id

    def set_id(self, card_id: str):
        self.__id = card_id

    def get_cc_number(self) -> str:
        return self.__cc_number

    def set_cc_number(self, cc_number: str):
        self.__cc_number = cc_number

    def get_cvv(self) -> str:
        return self.__cvv

    def set_cvv(self, cvv: str):
        self.__cvv = cvv

    def get_expiration_date(self) -> datetime:
        return self.__expiration_date

    def set_expiration_date(self, expiration_date: datetime):
        self.__expiration_date = expiration_date

    def get_billing_address(self) -> Address:
        return self.__billing_address

    def set_billing_address(self, billing_address: Address):
        self.__billing_address = billing_address



                      
