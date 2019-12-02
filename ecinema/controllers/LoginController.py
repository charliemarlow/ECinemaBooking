import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from ecinema.models.UserFactory import create_user

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
        else:
            error = "User {} does not exist".format(username)

        if error is None and user is not None:
            setup_session(user.get_username(), loggedin)
            if user.is_admin():
                return redirect(url_for('AdminController.admin'))
            else:
                return redirect(url_for('IndexController.index'))

        flash(error)

    return render_template('login.html')


def get_user(username: str):
    user = None
    customer = create_user('customer')
    admin = create_user('admin')
    customer_exists = customer.fetch(username)
    customer_exists = (customer_exists or
                       customer.fetch_by_email(username))

    if customer_exists:
        print("custy exists")
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
        customer = create_user('customer')

        g.user = customer.obj_as_dict(user_id)
        if g.user is not None:
            g.user = dict(g.user)
            g.user['is_admin'] = False

        # check for admin
        if g.user is None:
            admin = create_user('admin')
            if admin.fetch(user_id):
                g.user = dict(admin.obj_as_dict(user_id))
                g.user['is_admin'] = True
            else:
                session.clear()
                return redirect(url_for('IndexController.index'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('IndexController.index'))

@bp.route('/suspended')
def suspended():
    session.clear()
    return render_template('suspended.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        customer = create_user('customer')
        admin = create_user('admin')
        if g.user is None:
            return redirect(url_for('LoginController.login'))
        elif (customer.fetch(g.user['username']) and
              customer.get_status() == 'inactive'):
            return redirect(url_for('RegisterController.verify_account'))
        elif (customer.fetch(g.user['username']) and
              customer.get_status() == 'inactive'):
            return redirect(url_for('LoginController.suspended'))

        return view(**kwargs)

    return wrapped_view

# used for customer only things, like reviews
# won't let the admin login


def customer_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        print("Customer Login Required")
        customer = create_user('customer')
        fetched = customer.fetch(g.user['username'])
        if g.user is None:
            return redirect(url_for('LoginController.login'))
        elif not fetched or not customer.get_status() == 'active':
            if fetched:
                return redirect(url_for('LoginController.suspended'))
            return redirect(url_for('IndexController.index'))
        print(g.user['username'])
        return view(**kwargs)

    return wrapped_view


def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        admin = create_user('admin')
        if g.user is None:
            return redirect(url_for('LoginController.login'))
        elif not admin.fetch(g.user['username']):
            return redirect(url_for('IndexController.index'))

        return view(**kwargs)

    return wrapped_view
