import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from ecinema.models.Customer import Customer
from ecinema.models.Admin import Admin

from ecinema.tools.validation import (
    validate_name, validate_password
)

bp = Blueprint('LoginController', __name__, url_prefix='/')


def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            return redirect(url_for('IndexController.index'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
@logout_required
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        loggedin = request.form.get('loggedin')
        loggedin = False if loggedin is None else True

        user = get_user(username)

        error = None
        if user is not None:
            error = verify_username_password(username, password,
                                             user.get_password())

        if error is None and user is not None:
            setup_session(user.get_username(), loggedin)
            return redirect(url_for('IndexController.index'))

        flash(error)

    return render_template('login.html')


def get_user(username: str):
    user = None
    customer = Customer()
    admin = Admin()
    customer_exists = customer.fetch(username)

    if customer_exists:
        user = customer
    else:
        user = admin if admin.fetch(username) else None

    return user


def setup_session(user: str, remember_me: bool):
    session.clear()
    session['user_id'] = user
    session.permanent = remember_me


def verify_username_password(user: str, password: str, db_pass: str) -> str:
    error = None
    if user is None:
        error = 'Incorrect username.'
    elif not validate_password(password, password):
        error = 'Incorrect password. Password must be at ' + \
            'least 8 characters with at least 1 uppercase ' + \
            'letter and at least 1 number.'
    elif not check_password_hash(db_pass, password):
        error = 'Incorrect password.'

    return error


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        customer = Customer()

        g.user = customer.obj_as_dict(user_id)

        # check for admin
        if g.user is None:
            admin = Admin()
            g.user = admin.obj_as_dict(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('IndexController.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('LoginController.login'))

        return view(**kwargs)

    return wrapped_view
