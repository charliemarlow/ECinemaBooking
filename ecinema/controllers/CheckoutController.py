import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session
)
from datetime import datetime

from ecinema.tools.clean import create_datetime_from_sql, clean_tickets, format_price
from ecinema.tools.validation import validate_name, validate_duration, validate_text, validate_year, validate_cvv, validate_cc_number, validate_zip, validate_state, validate_year, validate_expiration_date
from ecinema.tools.generate import generate_order_id

from ecinema.controllers.LoginController import customer_login_required

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Customer import Customer
from ecinema.models.Price import Price
from ecinema.models.Promo import Promo
from ecinema.models.Booking import Booking

bp = Blueprint('CheckoutController', __name__, url_prefix='/')


def clear_booking_info():
    if session.get('tickets'):
        del session['tickets']

    if session.get('promo'):
        del session['promo']

    if session.get('checkout'):
        del session['checkout']

    if session.get('showtime'):
        del session['showtime']

    if session.get('total'):
        del session['total']


def create_booking_objects():
    order_id = 0
    total = session['total']
    card_id = request.form['card_id']
    showtime_id = session['showtime']
    movie_id = get_movie_by_showtime(showtime_id).get_id()
    customer_id = get_current_customer().get_id()

    promo_id = None
    if session.get('promo'):
        promo_id = session['promo']['id']

    booking = Booking()
    booking.create(order_id=order_id,
                   total_price=total,
                   credit_card_id=card_id,
                   promo_id=promo_id,
                   movie_id=movie_id,
                   customer_id=customer_id,
                   showtime_id=showtime_id)

    unique_id = booking.get_id()
    order = generate_order_id(unique_id, showtime_id, movie_id)
    booking.set_order_id(order)
    booking.save()

    associate_tickets(booking.get_id())


def associate_tickets(booking_id):
    pass


def get_current_customer():
    customer = Customer()
    customer.fetch(g.user['username'])
    return customer


def get_movie_by_showtime(sid):
    movie = Movie()
    showtime = Showtime()
    showtime.fetch(sid)
    movie.fetch(showtime.get_movie_id())
    return movie


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

    current_tickets = []  # current list being created
    all_tickets = []  # final 2D array of tickets by types

    for t in tickets:
        current_type = t['type']
        if current_type != old_type:
            current_tickets[0]['checkout_price'] = format_price(
                current_tickets[0]['num_price'] * len(current_tickets))
            all_tickets.append(list(current_tickets))
            current_tickets.clear()

        current_tickets.append(dict(t))
        old_type = t['type']

    current_tickets[0]['checkout_price'] = format_price(
        current_tickets[0]['num_price'] * len(current_tickets))
    all_tickets.append(list(current_tickets))
    return all_tickets


def calculate_fees_and_total(subtotal):
    price = Price()
    tax_price = price.get_tax_price() * subtotal
    online_fee = price.get_online_fee()
    total = subtotal + tax_price + online_fee

    fees = [
        {'name': 'Taxes', 'amount': format_price(tax_price)},
        {'name': 'Online Booking', 'amount': format_price(online_fee)}
    ]

    if session.get('promo'):
        promo_amt = session['promo']['percent'] * subtotal
        promo_fee = {'name': 'Promo: {}'.format(session['promo']['name']),
                     'amount': "-" + format_price(promo_amt)}
        fees.append(promo_fee)
        total = total - promo_amt

    return fees, total


def apply_promo(promo):
    promo_code = request.form['coupon']

    if promo.fetch_by_code(promo_code):
        promo_dict = {'id': promo.get_id(),
                      'name': promo.get_code(),
                      'percent': float(promo.get_promo())}
        return promo_dict
    return None


@bp.route('/checkout', methods=('GET', 'POST'))
@customer_login_required
def checkout():

    if (not session.get('showtime') or
        not session.get('tickets') or
            not g.user.get('username')):
        return redirect(url_for('IndexController.index'))

    if request.method == 'POST':
        delete_id = request.form.get('delete_ticket')

        if request.form.get('coupon'):
            promo = Promo()
            session['promo'] = apply_promo(promo)
        elif delete_id:
            delete_ticket(delete_id)
        elif request.form.get('add_payment'):
            session['checkout'] = True
            return redirect(url_for('AccountController.make_payment'))
        elif request.form.get('checkout'):
            if request.form.get('card_id'):
                create_booking_objects()
                clear_booking_info()
                return redirect(
                    url_for('BookingController.payment_confirmation'))
            else:
                flash("Please choose a payment card to proceed with checkout")
        elif request.form.get('cancel'):
            clear_booking_info()
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

    fees, total = calculate_fees_and_total(subtotal)
    session['total'] = total

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
