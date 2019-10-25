import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.data.db import get_db
from ecinema.models.Customer import Customer
from ecinema.controllers.LoginController import login_required
from ecinema.data.CustomerData import CustomerData
from ecinema.data.AddressData import AddressData
from ecinema.tools.validation import (
    validateName, validateEmail, validateUniqueEmail
)

bp = Blueprint('AccountController', __name__, url_prefix='/')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    return render_template('account.html')


@bp.route('/editprofile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    customer = CustomerData()
    addr = AddressData()
    user_id = session.get('user_id')
    user = customer.get_user_info(user_id)
    cid = user['customer_id']
    db = get_db() # fix this

    if request.method == 'POST':
        first_name = request.form.get('first')
        last_name = request.form.get('last')
        email = request.form.get('email')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        error = ""
        if first_name is not None and validateName(first_name):
            customer.set_first_name(cid, first_name)

        if last_name is not None and validateName(last_name):
            customer.set_last_name(cid, last_name)

        if (email is not None and validateEmail(email)
            and not validateUniqueEmail(email, db)):
            customer.set_email(cid, email)
        elif email is not None:
            error = "Email is invalid or already in use"

        if street is not None:
            addr.set_street(cid, street)

        if city is not None:
            addr.set_city(cid, city)

        if state is not None:
            addr.set_state(cid, state)

        if zip_code is not None:
            addr.set_zip_code(cid, zip_code)

        flash(error)
    user = customer.get_user_info(user_id)
    print(user['first_name'])
    address = addr.get_address_info(user['customer_id'])
    if address is None:
        address = {
            'state' : 'State',
            'city' : 'City',
            'street' : 'Street',
            'zip_code' : 'ZIP Code'
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
def verify_password():
    return render_template('verify_password.html')


