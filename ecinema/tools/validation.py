import re


def validateEmail(email : str) -> bool:
    return re.match(
        '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*'
        '@'
        '(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$',
        email) is not None


def validateName(name : str) -> bool:
    return len(name) > 1 and len(name) < 100


def validatePassword(password : str, confirmation : str) -> bool:
    return (password == confirmation and len(password) >= 8 and
            bool(re.search(r'\d', password)) and
            any(char.isupper() for char in password))


def validateUsername(username : str, db) -> bool:
    # sql stuff here
    return (db.execute(
        'SELECT customer_id FROM customer WHERE username = ?',
        (username,)
    ).fetchone() is not None and db.execute(
        'SELECT admin_id FROM admin WHERE username = ?',
        (username,)
    ).fetchone() is not None)
