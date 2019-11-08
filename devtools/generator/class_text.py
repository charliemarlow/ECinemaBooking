
setup_id_template='''
        self.__{attr} = None'''

set_all_12='''
            self.set_{attr}({class_name}['{attr}'])'''

set_all_8='''
        self.set_{attr}({class_name}['{attr}'])'''

tup_template="self.get_{attr}()"

get_set_template='''
    def get_{attr}(self) -> str:
        return self.__{attr}

    def set_{attr}(self, {attr}: str):
        self.__{attr} = {attr}
'''

body = '''
from ecinema.models.model import Model
from ecinema.data.{capital_name}Data import {capital_name}Data

class {capital_name}(Model):

    def __init__(self):
        self.__id = None
{setup_id}
        self._Model__is_init = False
        self._Model__id = None
        self.__data_access = {capital_name}Data()

    def obj_as_dict(self, key: str):
        return self.__data_access.get_info(key)

    def get_all_{class_name}s(self):
        return self.__data_access.get_all_{class_name}s()

    def fetch(self, key: str):
        {class_name} = self.obj_as_dict(key)

        if {class_name} is not None:
            self.set_id({class_name}[{class_name}_id])
{set_all_indent_12}
            self.set_is_init()

            return True

        return False

    def create(self, **kwargs):
        {class_name} = {dicti}
        for key, value in kwargs.items():
            {class_name}[key] = value

{set_all_indent_8}
        self.set_is_init()

        member_tup = ({create_tup})

        self.set_id(self.__data_access.insert_info(member_tup))

    def save(self) -> bool:
        if not self.is_initialized():
            return False

        member_tup = ({save_tup})

        self.__data_access.update_info(member_tup)
        return True

    def delete(self, key: str):
        self.__data_access.delete(key)

{getter_set}
'''
