
from ecinema.models.model import Model
from ecinema.data.TicketData import TicketData


class Ticket(Model):

    def __init__(self):
        self.__id = None

        self.__showtime_id = None
        self.__booking_id = None
        self.__age = None
        self.__seat_number = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = TicketData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_tickets(self):
        return self.__data_access.get_all_tickets()

    def fetch(self, key: str):
        ticket = self.obj_as_dict(key)

        if ticket is not None:
            self.set_id(ticket['ticket_id'])

            self.set_showtime_id(ticket['showtime_id'])
            self.set_booking_id(ticket['booking_id'])
            self.set_age(ticket['age'])
            self.set_seat_number(ticket['seat_number'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        ticket = {}
        for key, value in kwargs.items():
            ticket[key] = value

        self.set_showtime_id(ticket['showtime_id'])
        self.set_booking_id(ticket['booking_id'])
        self.set_age(ticket['age'])
        self.set_seat_number(ticket['seat_number'])
        self.set_is_init()

        member_tup = (
            self.get_showtime_id(),
            self.get_booking_id(),
            self.get_age(),
            self.get_seat_number())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (
            self.get_showtime_id(),
            self.get_booking_id(),
            self.get_age(),
            self.get_seat_number(),
            self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_showtime_id(self) -> str:
        return self.__showtime_id

    def set_showtime_id(self, showtime_id: str):
        self.__showtime_id = showtime_id

    def get_booking_id(self) -> str:
        return self.__booking_id

    def set_booking_id(self, booking_id: str):
        self.__booking_id = booking_id

    def get_age(self) -> str:
        return self.__age

    def set_age(self, age: str):
        self.__age = age

    def get_seat_number(self) -> str:
        return self.__seat_number

    def set_seat_number(self, seat_number: str):
        self.__seat_number = seat_number

    def is_available(self, seat, showtime):
        return self.__data_access.is_available(seat, showtime)
