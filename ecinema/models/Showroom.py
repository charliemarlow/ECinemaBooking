
from ecinema.models.model import Model
from ecinema.data.ShowroomData import ShowroomData

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

        member_tup = (self.get_theater_id(), self.get_num_seats(), self.get_showroom_name())

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = (self.get_theater_id(), self.get_num_seats(), self.get_showroom_name(), self.get_id())

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
