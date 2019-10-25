import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.data.db import get_db
from ecinema.models.Customer import Customer
from ecinema.controllers.LoginController import login_required

bp = Blueprint('AccountController', __name__, url_prefix='/')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    return render_template('account.html')


@bp.route('/editprofile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    user = {
        'first_name' : 'Charlie',
        'last_name' : 'Marlow',
        'email' : 'charmarlw@gmail.com',
        'promo' : 'True'
    }
    address = {
        'street' : '742 Oconee St',
        'city' : 'Athens',
        'state' : 'GA',
        'zip' : '30064'
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


