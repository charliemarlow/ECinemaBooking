import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.models.Customer import Customer

from ecinema.controllers.LoginController import (
    login_required, verify_username_password, get_user
)

from ecinema.data.CustomerData import CustomerData
from ecinema.data.AddressData import AddressData

from ecinema.tools.validation import (
    validate_name, validate_email, validate_unique_email
)

bp = Blueprint('AccountController', __name__, url_prefix='/')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    return render_template('account.html')


@bp.route('/editprofile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    customer = Customer()
    addr = AddressData()
    user_id = session.get('user_id')
    user = customer.obj_as_dict(user_id)
    cid = user['customer_id']

    if request.method == 'POST':
        first_name = request.form.get('first')
        last_name = request.form.get('last')
        email = request.form.get('email')
        subscribe = request.form.get('subscribe') is not None
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        error = ""
        if first_name is not None and validate_name(first_name):
            customer.set_first_name(cid, first_name)

        if last_name is not None and validate_name(last_name):
            customer.set_last_name(cid, last_name)

        if (email is not None and validate_email(email)
                and validate_unique_email(email)):
            customer.set_email(cid, email)
        elif email is not None:
            error = "Email is invalid or already in use"

        # TODO: fix subscribe

        if street is not None:
            addr.set_street(cid, street)

        if city is not None:
            addr.set_city(cid, city)

        if state is not None:
            addr.set_state(cid, state)

        if zip_code is not None:
            addr.set_zip_code(cid, zip_code)

        flash(error)
    print(user['first_name'])
    address = addr.get_info(user['customer_id'])
    print("\n\n")
    print(address)
    if address is None:
        address = {
            'state': 'State',
            'city': 'City',
            'street': 'Street',
            'zip_code': 'ZIP Code'
        }

    return render_template('editprofile.html', user=user, address=address)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('LoginController.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/manage_payment', methods=('GET', 'POST'))
def manage_payment():
    return render_template('manage_payment.html')


@bp.route('/make_payment', methods=('GET', 'POST'))
def make_payment():
    return render_template('make_payment.html')


@bp.route('/verify_password', methods=('GET', 'POST'))
@login_required
def verify_password():
    # use previous tools to verify the password
    if request.method == 'POST':
        username = session['user_id']
        password = request.form['password']

        user = get_user(username)

        error = None

        if user is not None:
            error = verify_username_password(username, password,
                                             user.get_password())
        if error is None and user is not None:
            return redirect(
                url_for('ResetPasswordController.reset_password')
            )

        flash(error)

    return render_template('verify_password.html')
