from ecinema.data.db import get_db


def is_new_email(email: str):
    db = get_db()
    return (db.execute(
        'SELECT customer_id FROM customer WHERE email = ?',
        (email,)
    ).fetchone() is None)


def is_unique_username(username: str):
    db = get_db()
    return (db.execute(
        'SELECT customer_id FROM customer WHERE username = ?',
        (username,)
    ).fetchone() is None and db.execute(
        'SELECT admin_id FROM admin WHERE username = ?',
        (username,)
    ).fetchone() is None)

# eventually fix this


def is_active_user(email: str) -> bool:
    db = get_db()
    status = db.execute(
        'SELECT status FROM customer WHERE email = ?',
        (email,)
    ).fetchone()

    if status is not None:
        return True if status['status'] == 'active' else False
    return False
