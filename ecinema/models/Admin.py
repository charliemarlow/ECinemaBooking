
from ecinema.models.model import Model
from ecinema.models.User import User
from ecinema.data.AdminData import AdminData


class Admin(Model, User):

    def __init__(self):
        self.__data_access = AdminData()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def fetch(self, key: str) -> bool:
        admin = self.obj_as_dict(key)
        if admin is not None:
            self.set_id(admin['admin_id'])
            self.set_username(admin['username'])
            self.set_password(admin['password'])
            self.set_is_init()
            return True
        return False

    def create(self, **kwargs):
        admin = {}
        for key, value in kwargs.items():
            user[key] = value

        self.set_username(admin['username'])
        self.set_password(admin['password'])
        self.set_is_init()

        member_tup = (self.get_username(),
                      self.get_password())
        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False
        member_tup = (self.get_username(),
                      self.get_password(),
                      self.get_username())
        self.__data_access.update_info(member_tup)
        return True

    def is_admin(self) -> bool:
        return True
