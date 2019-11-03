from datetime import datetime
from ecinema.tools.validation import validate_year

def clean_phone(phone: str) -> str:
    num = ""
    for c in phone:
        if not (c == ' ' or c == '-' or
            c =='(' or c == ')' or c == '+'):
            num = num + c

    return num

def clean_expiration(month: str, year: str):
    exp_date = datetime.now()
    error = None
    if validate_year(year):
        exp_date = datetime(int(year),
                             int(month[0:2]),
                             1, 1, 1)
    else:
        error = "Invalid year"

    return exp_date, error
