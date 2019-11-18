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
from ecinema.models.Price import Price

bp = Blueprint('BookingController', __name__, url_prefix='/')

@customer_login_required
@bp.route('/confirm_booking', methods=('GET', 'POST'))
def confirm_booking():

    if session.get('tickets') is None or session.get('tickets') == '':
        return redirect(url_for('IndexController.index'))

    if request.method == 'POST':
        delete_id = request.form.get('delete_ticket')
        if delete_id != '':
            delete_id = int(delete_id)
            tickets = session['tickets']
            del session['tickets']

            if len(tickets) == 1:
                return redirect(url_for('BookingController.cancel_booking'))
            else:
                del tickets[delete_id]

            session['tickets'] = tickets


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
    tickets = []
    ticket = {}
    subtotal = 0
    tid = 0
    for t in session['tickets']:
        ticket['tid'] = tid
        tid = tid + 1
        ticket['seat'] = t[0]
        ticket['type'] = t[1]

        # fetch a price object for that type
        # use get price to get the actual price
        price = Price()
        price.fetch(ticket['type'])
        price_amt = price.get_price()
        ticket['price'] = "${0:.2f} USD".format(price_amt)
        subtotal = subtotal + price_amt

        tickets.append(dict(ticket))

    # then calculate subtotal for the customer
    subtotal = "${0:.2f} USD".format(subtotal)

    return render_template('cart.html', tickets=tickets,
                           movie=movie.obj_as_dict(movie.get_id()),
                           showtime=showtime.get_time(),
                           subtotal=subtotal)


@customer_login_required
@bp.route('/cancel_booking', methods=('GET', 'POST'))
def cancel_booking():
    return render_template("bookingfail.html")
