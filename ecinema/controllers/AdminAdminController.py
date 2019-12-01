
import functools


from werkzeug.security import generate_password_hash

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_username, validate_password
)

from ecinema.models.UserFactory import create_user

bp = Blueprint('AdminAdminsController', __name__, url_prefix='/')


'''
************

NEED TO ADD TO __INIT__ WHEN READY


**************


'''

@bp.route('/manage_admin', methods=('GET', 'POST'))
@admin_login_required
def manage_admins():
    admin = create_user('admin')

    if request.method == 'POST':
        print("posted")
        delete_admin_id = request.form.get('delete_admin_id')
        edit_admin_id = request.form.get('edit_admin_id')

        print(delete_admin_id)
        if delete_admin_id and admin.fetch_by_id(delete_admin_id):
            # logic for deleting admins
            print("deleting")
            admin.delete(delete_admin_id)
        elif edit_admin_id != None and admin.fetch_by_id(edit_admin_id):
            return redirect(url_for('AdminAdminsController.edit_admin', a_id=edit_admin_id))

    # get a list of all admins
    admins = admin.get_all_admins()

    return render_template('manage_admin.html', admins=admins)

@bp.route('/edit_admin/<a_id>', methods=('GET', 'POST'))
@admin_login_required
def edit_admin(a_id):
    admin_id = a_id
    admin = create_user('admin')
    print(admin.fetch(admin_id))

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        error = None

        if username != '' and not validate_username(username):
            error = "username is invalid"
        elif username != '':
            admin.set_username(username)

        if password != '' and not validate_password(password):
            error = "password is invalid"
        elif password != '':
            admin.set_password(password)


        admin.save()

        if error is not None:
            flash(error)


    info = admin.obj_as_dict(admin_id)
    return render_template('edit_admin.html', admin=info)

@bp.route('/create_admin', methods=('GET', 'POST'))
@admin_login_required
def create_admin():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirmation']
        # validate all data, everything must be correct
        error = None

        admin = create_user('admin')

        if not admin.validate_username(username):
            error = "Username is already taken"
        elif not validate_password(password, confirm):
            error = 'Password is required and must be at least 8 '\
                + 'characters with 1 uppercase, and 1 number'


        if error is None:
            # if error is None, create a admin
            new_admin = create_user('admin')
            new_admin.create(username=username,
                             password=generate_password_hash(password))

            # then return to add admin
            return redirect(url_for('AdminAdminsController.manage_admins'))

        flash(error)


    return render_template('create_admin.html')
