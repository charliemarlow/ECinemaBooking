import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.db import get_db
from ecinema.validation import validateName, validatePassword, validateEmail, validateUsername
from ecinema.models.Customer import Customer

bp = Blueprint('IndexController', __name__, url_prefix='/')

@bp.route('/index')
def index():
    return render_template('web/index.html')
