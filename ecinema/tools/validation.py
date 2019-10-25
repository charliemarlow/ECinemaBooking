import re
from werkzeug.security import check_password_hash

'''
Place any code for validating user input here
Anywhere in the code base can access these by using
from ecinema.tools.validation import validateEmail, etc
'''

def validateEmail(email: str) -> bool:
    return re.match(
        '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*'
        '@'
        '(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
        email) is not None


def validateName(name: str) -> bool:
    return len(name) > 1 and len(name) < 100


def validatePassword(password: str, confirmation: str) -> bool:
    return (password == confirmation and len(password) >= 8 and
            bool(re.search(r'\d', password)) and
            any(char.isupper() for char in password))


def validateUsername(username: str, db) -> bool:
    # sql stuff here
    return (db.execute(
        'SELECT customer_id FROM customer WHERE username = ?',
        (username,)
    ).fetchone() is not None and db.execute(
        'SELECT admin_id FROM admin WHERE username = ?',
        (username,)
    ).fetchone() is not None)

def validate_new_password(new_password, username: str, db) -> bool:
    password = db.execute(
        'SELECT * FROM customer WHERE username = ?',
        (username,)
    ).fetchone()
    return not check_password_hash(password['password'], new_password)
