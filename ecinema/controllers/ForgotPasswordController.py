import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.tools.validation import (
    validate_name, validate_password, validate_email,
    validate_username, validate_unique_email, validate_user_status
)
from ecinema.tools.sendEmail import send_email

from ecinema.controllers.LoginController import setup_session

from ecinema.models.Customer import Customer

from itsdangerous import URLSafeTimedSerializer
import datetime

# from ecinema.token import generate_confirmation_token, confirm_token

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
        customer = Customer()

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
            token = generate_confirmation_token(email)

            # send the email (check out tools/sendEmail.py)
            subject = "Forgot Password?"

            # TODO: send an email of a link that can be clicked on
            # instead of just plaintext
            message = """Hey

            A forgot password request has been made for your account """\
                + """at Ecinema Booking. Please follow this link """\
                + """to reset your email. If you did not request this """\
                + """then please ignore this email"""\
                + """Link: http://127.0.0.1:5000/confirm/{}"""\
                + """

Best,

E-Cinema Booking
        """
            message = message.format(token)

            send_email(email, subject, message)


            # talk to me about handling it
            return render_template('forgotconfirmation.html')

        flash(error)

    return render_template('forgot.html')



def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('IAMSOFLUBINSECUREuuKEY')
    return serializer.dumps(email,
                            salt=
                            'THl72DfWa36wdEPJOEGbe71GSCDWADuuSALT')


def confirm_token(token, expiration=1200):
    serializer = URLSafeTimedSerializer('IAMSOFLUBINSECUREuuKEY')
    try:
        email = serializer.loads(
            token,
            salt='THl72DfWa36wdEPJOEGbe71GSCDWADuuSALT',
            max_age=expiration
        )
    except:
        return False
    return email


@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except BaseException:
        flash('The confirmation link is invalid or has expired.',
              'danger')
        # make a page explaining this to the user
        # TODO: make this point to forgot password fail page
        return redirect(url_for('IndexController.index'))
    customer = Customer()
    if customer.fetch_by_email(email):
        # log user in, redirect to reset password
        setup_session(customer.get_username(), False)

        return redirect(url_for('ResetPasswordController.reset_password'))

    # TODO: make this point to forgot password fail page
    return redirect(url_for('IndexController.index'))
