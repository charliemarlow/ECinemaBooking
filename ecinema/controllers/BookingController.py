import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session
)
from datetime import datetime

from ecinema.tools.clean import create_datetime_from_sql
from ecinema.tools.validation import validate_name, validate_duration, validate_text

from ecinema.controllers.LoginController import customer_login_required

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Showroom import Showroom
from ecinema.models.Review import Review
from ecinema.models.Customer import Customer

bp = Blueprint('BookingController', __name__, url_prefix='/')

@customer_login_required
@bp.route('/confirm_booking', methods=('GET', 'POST'))
def confirm_booking():
    #CONFIRM BOOKING
    # we'll pass this to the booking confirmation/summary page
    # then we set the booking timer to hold those tickets
    # where we'll calculate the total price

    # need to process these into a list for each ticket type
    for ticket in session['tickets']:
        print(ticket)

    return render_template('cart.html')
