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
    today = datetime.now()
    valid_year = expiration_date.year > today.year
    valid_month = expiration_date.year == today.year and expiration_date.month > today.month
    return valid_year or valid_month

def validate_phone(phone: str):
    num = ""
    for c in phone:
        if not (c == ' ' or c == '+' or c == '-' or c == '(' or c == ')'):
            num = num + c

    return len(num) == 10 or len(num) == 11

def validate_zip(zip_code: str):
    try:
        return is_real(zip_code)
    except ValueError:
        return False

def validate_year(year: str):
    return len(year) == 4

def validate_state(state: str):
    state = state.upper()
    return len(state) == 2 and state in state_dict

def validate_address(street: str, city: str, state: str, zip_code: str) -> str:
    error = None
    if (street != '' and city != '' and
        state != '' and zip_code != ''):
        if not validate_zip(zip_code):
            error = 'Zip code must be a valid zip code and '\
                + 'be entered in ##### or #####-#### format'
        elif not validate_state(state):
            error = 'State must be valid and entered in ## format'
    else:
        error = "To create a new address, all address information is required with zip code in #####-#### format and state in ## format"

    return error

def validate_card(card_type: str, card_number: str, expiration: datetime, cvv: str):
    error = None
    if (card_type != '' and card_number != '' and
        expiration is not None and cvv != ''):
         if not validate_cc_number(card_number):
             error = "Invalid credit card number"
         elif not validate_cvv(cvv):
             error = "Invalid CVV"
         elif not validate_expiration_date(expiration):
             error = "Invalid expiration date"
         elif card_type not in ['amex', 'master',
                               'visa', 'discover']:
             error = "Invalid card type"
    else:
        error = "To create a new credit card, all fields for the credit card are required"

    return error
