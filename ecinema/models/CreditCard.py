from ecinema.models.model import Model
from ecinema.data.CreditCardData import CreditCardData
from ecinema.models.Address import Address
from datetime import datetime


class CreditCard(Model):

    def __init__(self):
        self.__id = None
        self.__customer_id = None
        self.__cc_number = None
        self.__last_four = None
        self.__cvv = None
        self.__expiration_date = None
        self.__address = None
        self.__type = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = CreditCardData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def fetch(self, key: str):
        card = self.obj_as_dict(key)
        if card is not None:
            self.set_id(card['card_id'])
            self.set_customer(card['cid'])
            self.set_address(card['aid'])
            self.set_cc_number(card['card_number'])
            self.set_last_four(card['last_four'])
            self.set_cvv(card['cvv'])
            self.set_expiration_date(card['exp_date'])
            self.set_type(card['type'])
            self.set_is_init()
            return True

        return False

    def create(self, **kwargs):
        card = {}
        for key, value in kwargs.items():
            card[key] = value

        self.set_cc_number(card['card_number'])
        self.set_customer(card['customer_id'])
        self.set_address(card['address_id'])
        self.set_last_four(card['last_four'])
        self.set_cvv(card['cvv'])
        self.set_expiration_date(card['exp_date'])
        self.set_type(card['cardtype'])
        self.set_is_init()

        member_tup = (self.get_customer(), self.get_address(),
                      self.get_cc_number(), self.get_last_four(),
                      self.get_cvv(), self.get_expiration_date(),
                      self.get_type()
                      )

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> str:
        if not self.is_initialized():
            return False

        member_tup = (self.get_customer(),
                      self.get_address(), self.get_cc_number(),
                      self.get_cvv(), self.get_expiration_date(),
                      self.get_type(), self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

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

    def get_address(self) -> str:
        return self.__address

    def set_address(self, billing_address: str):
        self.__address = billing_address

    def get_customer(self) -> str:
        return self.__customer_id

    def set_customer(self, customer_id: str):
        self.__customer_id = customer_id

    def get_last_four(self) -> str:
        return self.__last_four

    def set_last_four(self, last_four: str):
        self.__last_four = last_four

    def get_type(self) -> str:
        return self.__type

    def set_type(self, card_type: str):
        self.__type = card_type
