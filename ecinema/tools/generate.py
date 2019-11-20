from math import floor
from random import random
from string import ascii_letters


def generate_username(name: str, customer_id: str):
    return name + "_" + str(random_int()) + \
        str(customer_id) + str(random_int())


def random_int():
    return floor(random() * 10)


def random_char():
    return str(ascii_letters[random_int()]).upper()


def generate_order_id(unique_id, sid, mid):
    return "#" + random_char() + str(unique_id) + random_char() + str(sid) + \
        random_char() + random_char() + str(mid)
