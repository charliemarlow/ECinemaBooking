import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.data.db import get_db
from ecinema.models.Customer import Customer
from ecinema.tools.validation import (
    validateName, validatePassword, validateEmail,
    validateUsername, validateUniqueEmail, validate_user_status
)
from itsdangerous import URLSafeTimedSerializer
from ecinema import app

bp = Blueprint('ForgotPasswordController', __name__, url_prefix='/')

@bp.route('/forgot', methods=('GET', 'POST'))
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        db = get_db()
        # validate email address first
        # 1. valid email, 2. user exists
        # 3. user status is active
        # 4. not none
        error = None

        if email is None:
            error = 'Email is required'
        elif not validateEmail(email):
            error = 'Email is not valid'
        elif not validateUniqueEmail(email, db):
            error = 'Email not registered to a user'
        elif not validate_user_status(email, db):
            error = 'Account is inactive or suspended'

        # then send an email that they have to respond to quick
        if error is None:
            # Generate the token

            # send the email (check out tools/sendEmail.py)

            # talk to me about handling it
            return render_template('forgotconfirmation.html')

        flash(error)

    return render_template('forgot.html')
