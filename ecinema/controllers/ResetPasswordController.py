import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from ecinema.models.Customer import Customer
from ecinema.tools.validation import validate_password
from ecinema.controllers.LoginController import login_required

bp = Blueprint('ResetPasswordController', __name__, url_prefix='/')


@bp.route('/reset', methods=('GET', 'POST'))
@login_required
def reset_password():
    # if the submit button has been presselsd...
    if request.method == 'POST':
        # pull data from forms
        password = request.form['password']
        confirmation = request.form['confirm']
        user_id = session.get('user_id')
        error = None1

        customer = Customer()
        customer.fetch(user_id)
        print(user_id)

        # validate the fields
        # per issue 7, we'll change this to javascript
        if not validate_password(password, confirmation):
            error = 'Password is required and must be at least 8 '\
                + 'characters with 1 uppercase, and 1 number'
        elif check_password_hash(customer.get_password(),
                                 password):
            error = 'Password must be different from your old '\
                + 'password'

        # update the password
        if error is None and user_id is not None:
            customer.set_password(generate_password_hash(password))
            customer.save()

            customer.send_password_reset_email(customer.get_email(),
                                               customer.get_first_name())

            # TODO: change this to a password change confirm screen
            return redirect(url_for('AccountController.edit_profile'))

        flash(error)

    return render_template('reset.html')
