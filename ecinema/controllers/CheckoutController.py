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
from ecinema.models.Promo import Promo

bp = Blueprint('CheckoutController', __name__, url_prefix='/')

@bp.route('/checkout', methods=('GET', 'POST'))
@customer_login_required
def checkout():

    if (not session.get('showtime') or
        not session.get('tickets') or
        not g.user.get('username')):
        return redirect(url_for('IndexController.index'))

    promo_percent = None
    promo = None
    if request.method == 'POST':
        error = "TEST"
        print(error)

        if request.form.get('coupon'):
            promo_code = request.form['coupon']
            print(promo_code)
            promo = Promo()

            if promo.fetch_by_code(promo_code):
                promo_percent = float(promo.get_promo())

        # need to verify all user information
        # verify the promo
        # then check card info
        # either verify new card info or not
        # either flash an error message
        # or create the booking object
        # then create the ticket(s) object(s)
        # then save and email the user, go to confirmation
        if error is None:
            return redirect(url_for('BookingController.payment_confirmation'))

    showtime = Showtime()
    showtime.fetch(session['showtime'])
    movie = Movie()
    movie.fetch(showtime.get_movie_id())
    tickets, subtotal = clean_tickets(session['tickets'])
    tickets = sorted(tickets, key=lambda k: k['type'])

    # sorry
    current_type = tickets[0]['type']
    old_type = tickets[0]['type']
    current_tickets = []
    all_tickets = []
    for t in tickets:
        current_type = t['type']
        if current_type != old_type:
            current_tickets[0]['price']  = '${0:.2f} USD'.format(current_tickets[0]['num_price'] * len(current_tickets) )
            all_tickets.append(list(current_tickets))
            current_tickets.clear()

        current_tickets.append(dict(t))
        old_type = t['type']

    current_tickets[0]['price']  = '${0:.2f} USD'.format(current_tickets[0]['num_price'] * len(current_tickets) )
    all_tickets.append(list(current_tickets))

    price = Price()
    tax_price = price.get_tax_price() * subtotal
    online_fee = price.get_online_fee()


    fees = [
        {'name': 'Taxes', 'amount': '${0:.2f} USD'.format(tax_price)},
        {'name': 'Online Booking', 'amount': '${0:.2f} USD'.format(online_fee)}
    ]
    total = subtotal + tax_price + online_fee

    if promo_percent is not None:
        promo_amt = promo_percent * subtotal
        promo_fee = {'name': 'Promo: {}'.format(promo.get_code()), 'amount': '(${0:.2f} USD)'.format(promo_amt)}
        fees.append(promo_fee)
        total = total - promo_amt


    total = "${0:.2f} USD".format(total)
    subtotal = "${0:.2f} USD".format(subtotal)

    return render_template('checkout.html',
                           showtime=showtime.get_time(),
                           movie=movie.get_title(),
                           tickets=all_tickets,
                           subtotal=subtotal,
                           total=total,
                           fees=fees)
