
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_duration, validate_name, validate_new_seats
)

from ecinema.models.Showroom import Showroom
from ecinema.models.Showtime import Showtime

bp = Blueprint('AdminPriceController', __name__, url_prefix='/')


@bp.route('/edit_prices', methods=('GET', 'POST'))
@admin_login_required
def manage_showrooms():
    showroom = Showroom()
