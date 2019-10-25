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

bp = Blueprint('TestController', __name__, url_prefix='/')


@bp.route('/manage_payment', methods=('GET', 'POST'))
def manage_payment():
    return render_template('manage_payment.html')

@bp.route('/make_payment', methods=('GET', 'POST'))
def make_payment():
    return render_template('make_payment.html')

@bp.route('/verify_password', methods=('GET', 'POST'))
def verify_password():
    return render_template('verify_password.html')
