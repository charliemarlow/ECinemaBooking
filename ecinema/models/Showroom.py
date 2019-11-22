
from ecinema.models.model import Model
from ecinema.data.ShowroomData import ShowroomData
from ecinema.models.Movie import Movie
from datetime import datetime, timedelta
from ecinema.data.db import get_db


class Showroom(Model):

    def __init__(self):
        self.__id = None

        self.__theater_id = None
        self.__num_seats = None
        self.__showroom_name = None
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = ShowroomData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_showrooms(self):
        return self.__data_access.get_all_showrooms()

    def fetch(self, key: str):
        showroom = self.obj_as_dict(key)

        if showroom is not None:
            self.set_id(showroom['showroom_id'])
            self.set_theater_id(showroom['theater_id'])
            self.set_num_seats(showroom['num_seats'])
            self.set_showroom_name(showroom['showroom_name'])
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        showroom = {}
        for key, value in kwargs.items():
            showroom[key] = value

        self.set_theater_id(showroom['theater_id'])
        self.set_num_seats(showroom['num_seats'])
        self.set_showroom_name(showroom['showroom_name'])
        self.set_is_init()

        member_tup = (
            self.get_theater_id(),
            self.get_num_seats(),
            self.get_showroom_name())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (
            self.get_theater_id(),
            self.get_num_seats(),
            self.get_showroom_name(),
            self.get_id())

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

    def get_theater_id(self) -> str:
        return self.__theater_id

    def set_theater_id(self, theater_id: str):
        self.__theater_id = theater_id

    def get_num_seats(self) -> str:
        return self.__num_seats

    def set_num_seats(self, num_seats: str):
        self.__num_seats = num_seats

    def get_showroom_name(self) -> str:
        return self.__showroom_name

    def set_showroom_name(self, showroom_name: str):
        self.__showroom_name = showroom_name

    def unique_name(self, name: str) -> bool:
        return self.__data_access.unique_name(name)

    def __convert_sql_time(self, stime):
        year = int(stime[0:4])
        month = int(stime[5:7])
        day = int(stime[8: 10])

        hour = int(stime[11:13])
        minute = int(stime[14:16])

        return datetime(year, month, day, hour, minute, 0)

    def check_availability(self, dtime: datetime, timeID,
                           myduration) -> bool:
        showtimes = self.__data_access.get_all_showtimes(self.get_id())
        myID = self.get_id()

        for time in showtimes:
            if (time is not None
                and time['showroom_id'] == myID
                    and time['showtime_id'] != timeID):

                othermovie = Movie()
                othermovie.fetch(time['movie_id'])

                duration = int(othermovie.get_duration())
                start_time = self.__convert_sql_time(time['time'])
                finish_time = start_time + timedelta(minutes=duration)

                my_start_time = dtime
                my_finish_time = my_start_time + timedelta(minutes=myduration)

                if my_start_time <= finish_time and start_time <= my_finish_time:
                    return False

        return True

    def has_showtimes(self):
        return len(self.__data_access.get_all_showtimes(self.get_id())) >= 1

    def update_num_seats(self, num_seats) -> bool:
        if self.is_initialized():

            current_seats = int(self.get_num_seats())
            num_seats = int(num_seats)
            diff = num_seats - current_seats
            myID = self.get_id()

            if current_seats <= num_seats:
                # for each showtime, update info
                self.__data_access.update_seat_number(diff, myID)
                return True
            elif current_seats > num_seats:
                if self.__data_access.check_valid_decrease(diff, myID):
                    self.__data_access.update_seat_number(diff, myID)
                    return True

        return False
