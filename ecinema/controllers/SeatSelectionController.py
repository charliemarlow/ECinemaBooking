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

bp = Blueprint('SeatSelectionController', __name__, url_prefix='/')

@customer_login_required
@bp.route('/select_seat', methods=('GET', 'POST'))
def select_seat():
    # INFO we need: showtime_id and customer
    print(session['showtime'])
    print(g.user['username'])
    showtime = Showtime()
    showtime.fetch(session['showtime'])
    showroom = Showroom()
    showroom.fetch(showtime.get_showroom_id())
    print(showroom.get_num_seats())
    tickets = showtime.get_all_tickets()

    # probably need to pull all tickets
    # for this showtime, and get a list of taken
    # seats to pass to zach
    available = range(showroom.get_num_seats())
    if len(tickets) > 0:
        for ticket in tickets:
            seat_no = int(ticket['seat_number'])
            available[seat_no - 1] = -1

    # ZACH:
    # from this page, we'll get the seats and their ages
    # we need to get an array of tuples like
    # [(seatNo, age),]
    example = [(12, "adult"), (11, "student")]
    print(session.get('tickets'))
    if session.get('tickets') is not None:
        session['tickets'] = session['tickets'] + example
    else:
        session['tickets'] = example

    #CHECKOUT
    # then we'll direct users to the checkout page
    # where we confirm their information and charge them

    #FINAL CONFIRMATION
    # then pass them on to the booking confirmation page
    # and send them an email
    return render_template("seat_selection.html", tickets=available)
