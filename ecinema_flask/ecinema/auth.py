import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.db import get_db
from ecinema.validation import validateName, validatePassword, validateEmail, validateUsername
from ecinema.models.Customer import Customer

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        confirmation  = request.form['confirm']
        username = request.form['userid']
        email = request.form['email']
        subscribe = 0 if request.form.get('subscribe') is None else 1

        db = get_db()
        error = None

        if not validateName(firstname):
            print(firstname)
            error = "First name is required"
        elif not validateName(lastname):
            error = "Last name is required"
        elif not validatePassword(password, confirmation):
            error = 'Password is required and must be at least 8 characters with 1 uppercase, and 1 number'
        elif not username:
            error = 'Username is required'
        elif not validateEmail(email):
            error = 'Email is required and must be valid'
        elif validateUsername(username, db):
            error = 'Username {} is already taken.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO customer (first_name, last_name, email, subscribe_to_promo, username, password) VALUES (?, ?, ?, ?, ?, ?)',
                (firstname, lastname, email, subscribe, username, generate_password_hash(password))
            )
            db.commit()

            customer = Customer.Customer()
            customer.sendConfirmationEmail(email, firstname)

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('web/registration.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        loggedin = request.form.get('loggedin')
        loggedin = False if loggedin is None else True

        db = get_db()
        user = db.execute(
            'SELECT * FROM customer WHERE username = ?', (username,)
        ).fetchone()

        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('index'))

        flash(error)

    return render_template('web/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/index')
def index():
    return render_template('web/index.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
