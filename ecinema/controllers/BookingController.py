import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session, current_app, Flask
)
import datetime

from ecinema.tools.clean import create_datetime_from_sql, clean_tickets, format_seat
from ecinema.tools.validation import validate_name, validate_duration, validate_text
from ecinema.tools.clean import create_datetime_from_sql, format_price
from ecinema.controllers.LoginController import customer_login_required

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Showroom import Showroom
from ecinema.models.Review import Review
from ecinema.models.Price import Price
from ecinema.models.Ticket import Ticket
from ecinema.models.Booking import Booking

bp = Blueprint('BookingController', __name__, url_prefix='/')


@bp.route('/cancel_booking', methods=('GET', 'POST'))
@customer_login_required
def cancel_booking():
    return render_template("bookingfail.html")


@bp.route('/payment_confirmation/<bid>', methods=('GET', 'POST'))
@customer_login_required
def payment_confirmation(bid):

    confirm = False
    if bid[-1] == 'c':
        bid = bid[0:-1]
        confirm = True

    fees = []

    booking = Booking()
    if not booking.fetch(bid):
        return redirect(url_for('IndexController.index'))

    movie = Movie()
    movie = movie.obj_as_dict(booking.get_movie_id())
    showtime = Showtime()
    showtime.fetch(booking.get_showtime_id())

    tkts = booking.get_tickets()
    tickets = []
    for t in tkts:
        t = dict(t)
        t['seat_number'] = format_seat(t['seat_number'])
        tickets.append(t)

    booking = dict(booking.obj_as_dict(bid))
    booking['order_date'] = create_datetime_from_sql(booking['order_date'])
    booking['total_price'] = format_price(booking['total_price'])
    return render_template('confirmation.html',
                           tickets=tickets,
                           fees=fees,
                           movie=movie,
                           showtime=showtime.get_time(),
                           booking=booking,
                           confirm=confirm)
