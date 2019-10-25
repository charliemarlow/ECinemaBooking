import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.data.db import get_db
from ecinema.models.Customer import Customer
from ecinema.tools.validation import (
    validateName, validatePassword, validateEmail, validateUsername
)

bp = Blueprint('ForgotPasswordController', __name__, url_prefix='/')


@bp.route('/forgot', methods=('GET', 'POST'))
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        # validate email address first
        # 1. valid email, 2. user exists
        # 3. user status is active
        # 4. not none
        error = None

        if email is None:
            error = 'Email is required'
        elif not validateEmail(email):
            error = 'Email is not valid'

        # then send an email that they have to respond to quick

        # then go into reset password stuff

        flash(error)
    # need to
    return render_template('forgot.html')
