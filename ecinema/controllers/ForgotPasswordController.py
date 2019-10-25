import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.tools.validation import (
    validate_name, validate_password, validate_email,
    validate_username, validate_unique_email, validate_user_status
)
from itsdangerous import URLSafeTimedSerializer
import datetime

#from ecinema.token import generate_confirmation_token, confirm_token

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
            token = generate_confirmation_token(email)

            # Generate the token

            # send the email (check out tools/sendEmail.py)

            # talk to me about handling it
            return render_template('forgotconfirmation.html')

        flash(error)

    return render_template('forgot.html')


'''
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['IAMSOFLUBINSECUREuuKEY'])
    return serializer.dumps(email, salt=app.config['THl72DfWa36wdEPJOEGbe71GSCDWADuuSALT'])


def confirm_token(token, expiration=1200):
    serializer = URLSafeTimedSerializer(app.config['IAMSOFLUBINSECUREuuKEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['THl72DfWa36wdEPJOEGbe71GSCDWADuuSALT'],
            max_age=expiration
        )
    except:
        return False
    return email
'''

@bp.route('/confirm_user/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))
