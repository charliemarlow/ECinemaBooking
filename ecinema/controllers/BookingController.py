import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session
)
from datetime import datetime

from ecinema.tools.clean import create_datetime_from_sql, clean_tickets
from ecinema.tools.validation import validate_name, validate_duration, validate_text

from ecinema.controllers.LoginController import customer_login_required

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Showroom import Showroom
from ecinema.models.Review import Review
from ecinema.models.Customer import Customer
from ecinema.models.Price import Price

bp = Blueprint('BookingController', __name__, url_prefix='/')


@bp.route('/confirm_booking', methods=('GET', 'POST'))
@customer_login_required
def confirm_booking():

    if not session.get('tickets') or not session.get('showtime'):
        return redirect(url_for('IndexController.index'))

    if request.method == 'POST':
        delete_id = request.form.get('delete_ticket')
        if delete_id:
            delete_id = int(delete_id)
            tickets = session['tickets']
            del session['tickets']

            if len(tickets) == 1:
                return redirect(url_for('BookingController.cancel_booking'))
            else:
                del tickets[delete_id]

            session['tickets'] = tickets
        elif request.form.get('cancel'):
            del session['tickets']
            return redirect(url_for('BookingController.cancel_booking'))


    # may want to refactor by creating a booking object when they tap on book ticket
    # then creating tickets during seat selection
    # so then we'd have an incomplete booking and ticket objects
    # then finish them during booking

    #CONFIRM BOOKING
    # we'll pass this to the booking confirmation/summary page
    # then we set the booking timer to hold those tickets
    # where we'll calculate the total price

    # we need to figure out
    # showtime date/time
    showtime = Showtime()
    showtime.fetch(session['showtime'])

    # movie name
    movie = Movie()
    movie.fetch(showtime.get_movie_id())

    # ticket type (from tickets)
    # ticket price
    tickets, subtotal = clean_tickets(session['tickets'])

    # then calculate subtotal for the customer
    subtotal = "${0:.2f} USD".format(subtotal)

    return render_template('cart.html',
                           tickets=tickets,
                           movie=movie.obj_as_dict(movie.get_id()),
                           showtime=showtime.get_time(),
                           subtotal=subtotal)



@bp.route('/cancel_booking', methods=('GET', 'POST'))
@customer_login_required
def cancel_booking():
    return render_template("bookingfail.html")

@bp.route('/payment_confirmation', methods=('GET', 'POST'))
@customer_login_required
def payment_confirmation():
    return render_template('confirmation.html')
