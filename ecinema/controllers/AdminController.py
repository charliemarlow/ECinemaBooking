import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required


bp = Blueprint('AdminController', __name__, url_prefix='/')


@bp.route('/admin')
@admin_login_required
def admin():
    return render_template('admin.html')
