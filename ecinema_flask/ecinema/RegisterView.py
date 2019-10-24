import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.db import get_db
from ecinema.validation import validateName, validatePassword, validateEmail, validateUsername
from ecinema.models.Customer import Customer

bp = Blueprint('RegisterView', __name__, url_prefix='/')

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

            customer = Customer()
            customer.sendConfirmationEmail(email, firstname)

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('web/registration.html')
