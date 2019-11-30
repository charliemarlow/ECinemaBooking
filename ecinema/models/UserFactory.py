from ecinema.models.Customer import Customer
from ecinema.models.Admin import Admin

def create_user(typ):
    targetclass = typ.capitalize()
    return globals()[targetclass]()

def create_new_user(**kwargs):
    if kwargs.get('first_name'):
        user = create_user('customer')
        user.create(**kwargs)
    else:
        user = create_user('admin')
        user.create(**kwargs)
    return user
