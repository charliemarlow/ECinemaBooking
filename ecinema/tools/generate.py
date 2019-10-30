from math import floor
from random import random

def generate_username(name: str, customer_id: str):
    return name + "_" + str(random_int()) + str(customer_id) + str(random_int())

def random_int():
    return floor(random() * 10)
