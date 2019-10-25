import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.tools.validation import (
    validate_name, validate_password, validate_email,
    validate_username, validate_unique_email, validate_user_status
)
from itsdangerous import URLSafeTimedSerializer

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
        elif not validate_email(email):
            error = 'Email is not valid'
        elif validate_unique_email(email):
            error = 'Email not registered to a user'
        elif not validate_user_status(email):
            error = 'Account is inactive or suspended'

        # then send an email that they have to respond to quick
        if error is None:

            # Generate the token

            # send the email (check out tools/sendEmail.py)

            # talk to me about handling it
            return render_template('forgotconfirmation.html')

        flash(error)

    return render_template('forgot.html')


'''
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=1200):
    serializer = URLSafeTimedSerializer(app.config['I AM SO FLUBIN SECURE'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['THl72DfWa36wdEPJOEGbe71GSCDWAD'],
            max_age=expiration
        )
    except:
        return False
    return email
'''
