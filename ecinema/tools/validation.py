import re
from werkzeug.security import check_password_hash
from ecinema.data.ValidationData import (
    is_new_email, is_unique_username,
    is_active_user
)
from datetime import datetime
from zipcodes import is_real
from ecinema.data.states import state_dict

'''
Place any code for validating user input here
Anywhere in the code base can access these by using
from ecinema.tools.validation import validateEmail, etc
'''


def validate_email(email: str) -> bool:
    return re.match(
        '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*'
        '@'
        '(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
        email) is not None


def validate_unique_email(email: str) -> bool:
    return is_new_email(email)


def validate_name(name: str) -> bool:
    return len(name) > 1 and len(name) < 100


def validate_password(password: str, confirmation: str) -> bool:
    return (password == confirmation and len(password) >= 8 and
            bool(re.search(r'\d', password)) and
            any(char.isupper() for char in password))


def validate_username(username: str) -> bool:
    return is_unique_username(username)


def validate_user_status(email: str) -> bool:
    return is_active_user(email)


def validate_cvv(cvv: str) -> bool:
    return len(cvv) > 2 and len(cvv) < 5


def validate_cc_number(cc_number: str) -> bool:
    return len(cc_number) > 12 and len(cc_number) < 20


def validate_expiration_date(expiration_date: datetime) -> bool:
    return (expiration_date.year > today.year) or (expiration_date.year == today.year and expiration_date.month > today.month)

def validate_phone(phone: str):
    num = ""
    for c in phone:
        if not (c == '+' or c == '-' or c == '(' or c == ')'):
            num = num + c

    return len(num) == 10 or len(num) == 11

def validate_zip(zip_code: str):
    return is_real(zip_code)

def validate_state(state: str):
    state = state.upper()
    return state in state_dict
