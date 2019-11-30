
from ecinema.models.model import Model
from ecinema.data.ShowtimeData import ShowtimeData
from ecinema.tools.clean import create_datetime_from_sql
from datetime import datetime


class Showtime(Model):

    def __init__(self):
        self.__id = None
        self.__time = None
        self.__available_seats = None
        self.__movie_id = None
        self.__showroom_id = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = ShowtimeData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_showtimes(self):
        return self.__data_access.get_all_showtimes()

    def fetch(self, key: str):
        showtime = self.obj_as_dict(key)

        if showtime is not None:
            self.set_id(showtime['showtime_id'])
            print(showtime['time'])
            self.set_time(create_datetime_from_sql(showtime['time']))
            self.set_available_seats(showtime['available_seats'])
            self.set_movie_id(showtime['movie_id'])
            self.set_showroom_id(showtime['showroom_id'])
            self.set_is_init()
            return True
        return False

    def create(self, **kwargs):
        showtime = {}
        for key, value in kwargs.items():
            showtime[key] = value

        self.set_time(showtime['time'])
        self.set_available_seats(showtime['available_seats'])
        self.set_movie_id(showtime['movie_id'])
        self.set_showroom_id(showtime['showroom_id'])
        self.set_is_init()

        member_tup = (self.get_time(), self.get_available_seats(),
                      self.get_movie_id(), self.get_showroom_id())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (self.get_time(), self.get_available_seats(),
                      self.get_movie_id(), self.get_showroom_id(),
                      self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_all_tickets(self):
        return self.__data_access.get_tickets(self.get_id())

    def get_time(self) -> datetime:
        return self.__time

    def set_time(self, time: datetime):
        self.__time = time

    def get_available_seats(self) -> str:
        return self.__available_seats

    def set_available_seats(self, available_seats: str):
        self.__available_seats = available_seats

    def increment_available_seats(self, available_seats: int):
        self.__available_seats = int(self.__available_seats) + int(available_seats)

    def get_movie_id(self) -> str:
        return self.__movie_id

    def set_movie_id(self, movie_id: str):
        self.__movie_id = movie_id

    def get_showroom_id(self) -> str:
        return self.__showroom_id

    def set_showroom_id(self, showroom_id: str):
        self.__showroom_id = showroom_id

    def validate_seats(self, showroom_id, num_seats):
        return self.__data_access.validate_seats(showroom_id, num_seats)
