import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session
)
from datetime import datetime

from ecinema.tools.clean import create_datetime_from_sql, clean_tickets, format_price
from ecinema.tools.validation import validate_name, validate_duration, validate_text, validate_year, validate_cvv, validate_cc_number, validate_zip, validate_state, validate_year, validate_expiration_date

from ecinema.controllers.LoginController import customer_login_required

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Showroom import Showroom
from ecinema.models.Review import Review
from ecinema.models.Customer import Customer
from ecinema.models.Price import Price
from ecinema.models.Promo import Promo

bp = Blueprint('CheckoutController', __name__, url_prefix='/')



def delete_ticket(delete_id):
    delete_id = int(delete_id)
    tickets = session['tickets']
    del session['tickets']

    if len(tickets) == 1:
        return redirect(url_for('BookingController.cancel_booking'))
    else:
        del tickets[delete_id]

    session['tickets'] = tickets

def get_ticket_type_lists(tickets):
    tickets = sorted(tickets, key=lambda k: k['type'])

    # initialize values for the first type
    current_type = tickets[0]['type']
    old_type = tickets[0]['type']

    current_tickets = [] # current list being created
    all_tickets = [] # final 2D array of tickets by types

    for t in tickets:
        current_type = t['type']
        if current_type != old_type:
            current_tickets[0]['checkout_price']  = format_price(current_tickets[0]['num_price'] * len(current_tickets) )
            all_tickets.append(list(current_tickets))
            current_tickets.clear()

        current_tickets.append(dict(t))
        old_type = t['type']

    current_tickets[0]['checkout_price']  = format_price(current_tickets[0]['num_price'] * len(current_tickets) )
    all_tickets.append(list(current_tickets))
    return all_tickets

def calculate_fees_and_total(subtotal, promo, promo_percent):
    price = Price()
    tax_price = price.get_tax_price() * subtotal
    online_fee = price.get_online_fee()
    total = subtotal + tax_price + online_fee

    fees = [
        {'name': 'Taxes', 'amount': format_price(tax_price)},
        {'name': 'Online Booking', 'amount': format_price(online_fee)}
    ]

    if promo_percent is not None:
        promo_amt = promo_percent * subtotal
        promo_fee = {'name': 'Promo: {}'.format(promo.get_code()),
                     'amount': "-" + format_price(promo_amt)}
        fees.append(promo_fee)
        total = total - promo_amt

    return fees, total


def apply_promo(promo):
    promo_code = request.form['coupon']

    if promo.fetch_by_code(promo_code):
        return float(promo.get_promo())
    return None

@bp.route('/checkout', methods=('GET', 'POST'))
@customer_login_required
def checkout():

    if (not session.get('showtime') or
        not session.get('tickets') or
        not g.user.get('username')):
        return redirect(url_for('IndexController.index'))

    '''
    for t in session['ticket_ids']:
        print(t)
    '''
    promo_percent = None
    promo = None
    if request.method == 'POST':
        error = None
        delete_id = request.form.get('delete_ticket')

        if request.form.get('coupon'):
            promo = Promo()
            promo_percent = apply_promo(promo)
        elif delete_id:
            delete_ticket(delete_id)
        elif request.form.get('add_payment'):
            # TODO: fix it so that it doesn't do away with promo info
            session['checkout'] = True
            return redirect(url_for('AccountController.make_payment'))
        elif request.form.get('checkout'):
            if request.form.get('card_id'):
                # TODO: create booking and go to confirmation
                return redirect(url_for('BookingController.payment_confirmation'))
            else:
                flash("Pick a card")
        elif request.form.get('cancel'):
            # TODO: Clean up
            return redirect(url_for('IndexController.index'))

        # need to verify all user information
        # verify the promo
        # then check card info
        # either verify new card info or not
        # either flash an error message
        # or create the booking object
        # then create the ticket(s) object(s)
        # then save and email the user, go to confirmation
        #        if error is None:
        #    return redirect(url_for('BookingController.payment_confirmation'))

    customer = Customer()
    customer.fetch(g.user['username'])
    cards = customer.get_all_cards()

    showtime = Showtime()
    showtime.fetch(session['showtime'])

    movie = Movie()
    movie.fetch(showtime.get_movie_id())

    tickets, subtotal = clean_tickets(session['tickets'])

    # Returns a 2D array of tickets
    # each list is a different type
    all_tickets = get_ticket_type_lists(tickets)

    fees, total = calculate_fees_and_total(subtotal,
                                           promo,
                                           promo_percent)

    total = format_price(total)
    subtotal = format_price(subtotal)

    return render_template('checkout.html',
                           showtime=showtime.get_time(),
                           movie=movie.obj_as_dict(movie.get_id()),
                           tickets=all_tickets,
                           subtotal=subtotal,
                           total=total,
                           fees=fees,
                           cards=cards)
