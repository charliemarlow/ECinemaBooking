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


@bp.route('/test', methods=('GET', 'POST'))
def test():
    return render_template('index_loggedin.html')
