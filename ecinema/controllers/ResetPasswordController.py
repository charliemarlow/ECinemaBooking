import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.data.db import get_db
from ecinema.models.Customer import Customer
from ecinema.tools.validation import validatePassword, validate_new_password
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

        db = get_db()
        error = None

        # validate the fields
        # per issue 7, we'll change this to javascript
        if not validatePassword(password, confirmation):
            error = 'Password is required and must be at least 8 '\
                + 'characters with 1 uppercase, and 1 number'
        elif not validate_new_password(password, user_id, db):
            error = 'Password must be different from your old '\
                + 'password'

        # update the password
        if error is None and user_id is not None:
            print("executing query")
            db.execute(
                'UPDATE customer SET password = ? WHERE username = ?',
                (generate_password_hash(password), user_id)
            )
            user = db.execute('SELECT * FROM customer WHERE username = ?', (user_id,)
            ).fetchone()
            db.commit()

            customer = Customer()
            customer.send_password_reset_email(user['email'],
                                               user['first_name'])

            return redirect(url_for('AccountController.edit_profile'))

        flash(error)

    return render_template('reset.html')
