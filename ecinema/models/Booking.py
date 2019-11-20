
from ecinema.models.model import Model
from ecinema.data.BookingData import BookingData


class Booking(Model):

    def __init__(self):
        self.__id = None

        self.__order_id = None
        self.__total_price = None
        self.__credit_card_id = None
        self.__promo_id = None
        self.__movie_id = None
        self.__customer_id = None
        self.__showtime_id = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = BookingData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_bookings(self):
        return self.__data_access.get_all_bookings()

    def fetch(self, key: str):
        booking = self.obj_as_dict(key)

        if booking is not None:
            self.set_id(booking['booking_id'])

            self.set_order_id(booking['order_id'])
            self.set_total_price(booking['total_price'])
            self.set_credit_card_id(booking['credit_card_id'])
            self.set_promo_id(booking['promo_id'])
            self.set_movie_id(booking['movie_id'])
            self.set_customer_id(booking['customer_id'])
            self.set_showtime_id(booking['showtime_id'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        booking = {}
        for key, value in kwargs.items():
            booking[key] = value

        self.set_order_id(booking['order_id'])
        self.set_total_price(booking['total_price'])
        self.set_credit_card_id(booking['credit_card_id'])
        self.set_promo_id(booking['promo_id'])
        self.set_movie_id(booking['movie_id'])
        self.set_customer_id(booking['customer_id'])
        self.set_showtime_id(booking['showtime_id'])
        self.set_is_init()

        member_tup = (
            self.get_order_id(),
            self.get_total_price(),
            self.get_credit_card_id(),
            self.get_promo_id(),
            self.get_movie_id(),
            self.get_customer_id(),
            self.get_showtime_id())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (
            self.get_order_id(),
            self.get_total_price(),
            self.get_credit_card_id(),
            self.get_promo_id(),
            self.get_movie_id(),
            self.get_customer_id(),
            self.get_showtime_id(),
            self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_order_id(self) -> str:
        return self.__order_id

    def set_order_id(self, order_id: str):
        self.__order_id = order_id

    def get_total_price(self) -> str:
        return self.__total_price

    def set_total_price(self, total_price: str):
        self.__total_price = total_price

    def get_credit_card_id(self) -> str:
        return self.__credit_card_id

    def set_credit_card_id(self, credit_card_id: str):
        self.__credit_card_id = credit_card_id

    def get_promo_id(self) -> str:
        return self.__promo_id

    def set_promo_id(self, promo_id: str):
        self.__promo_id = promo_id

    def get_movie_id(self) -> str:
        return self.__movie_id

    def set_movie_id(self, movie_id: str):
        self.__movie_id = movie_id

    def get_customer_id(self) -> str:
        return self.__customer_id

    def set_customer_id(self, customer_id: str):
        self.__customer_id = customer_id

    def get_showtime_id(self) -> str:
        return self.__showtime_id

    def set_showtime_id(self, showtime_id: str):
        self.__showtime_id = showtime_id
