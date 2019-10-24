import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.db import get_db
from ecinema.validation import validateName, validatePassword, validateEmail, validateUsername
from ecinema.models.Customer import Customer

bp = Blueprint('LoginController', __name__, url_prefix='/')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        loggedin = request.form.get('loggedin')
        loggedin = False if loggedin is None else True

        db = get_db()

        #check if username is in the user table
        user = db.execute(
            'SELECT * FROM customer WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            # check if the user is actually an admin
            user = db.execute(
                'SELECT * FROM admin WHERE username = ?', (username,)
            ).fetchone()

        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['username']
            session.permanent = loggedin
            print(session)
            return redirect(url_for('IndexController.index'))

        flash(error)

    return render_template('web/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM customer WHERE username = ?', (user_id,)
        ).fetchone()

        #check for admin
        if g.user is None:
            g.user = get_db().execute(
                'SELECT * FROM admin WHERE username = ?', (user_id,)
            ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('IndexController.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
