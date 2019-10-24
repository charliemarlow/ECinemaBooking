import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.db import get_db
from ecinema.validation import validateName, validatePassword, validateEmail, validateUsername
from ecinema.models.Customer import Customer

bp = Blueprint('EditProfileController', __name__, url_prefix='/')


@bp.route('/editprofile', methods=('GET', 'POST'))
def editProfile():
    if request.method == 'POST':
        # pull data from forms

        # IMPORTANT: non-required fields should use the .get method

        db = get_db()
        error = None

        # validate the fields
        # per issue 7, we'll change this to javascript
        # create a new user

    return render_template('editprofile.html')
