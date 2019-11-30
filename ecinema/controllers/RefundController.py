import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session, current_app, Flask
)
import datetime

from ecinema.tools.clean import create_datetime_from_sql, clean_tickets
from ecinema.tools.clean import create_datetime_from_sql, format_price
from ecinema.controllers.LoginController import customer_login_required

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Showroom import Showroom
from ecinema.models.Review import Review
from ecinema.models.Customer import Customer
from ecinema.models.Price import Price
from ecinema.models.Ticket import Ticket
from ecinema.models.Booking import Booking

bp = Blueprint('RefundController', __name__, url_prefix='/')


@bp.route('/previous_orders', methods=('GET', 'POST'))
@customer_login_required
def previous_orders():
    return render_template('orders.html')
