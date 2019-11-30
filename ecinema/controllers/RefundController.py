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

def refund_booking(bid):
    # clean up
    # delete all tickets, reset showtime incrementer
    # delete the booking object
    # send an email!
    return

def process_tickets(tickets):
    tickets = sorted(tickets, key=lambda k: k['age'])
    current_type = tickets[0]['age']
    old_type = current_type

    current_tickets = []
    all_tickets = []

    for t in tickets:
        current_type = t['age']
        if current_type != old_type:
            all_tickets.append(list(current_tickets))
            current_tickets.clear()
        current_tickets.append(dict(t))
        old_type = t['age']

    all_tickets.append(list(current_tickets))
    return all_tickets


def process_bookings(bookings):
    refund_info = {}
    refunds = []

    for booking in bookings:
        refund_info['order_no'] = booking['order_id']
        refund_info['total'] = format_price(booking['total_price'])
        refund_info['bid'] = booking['booking_id']

        # get tickets
        booking_obj = Booking()
        booking_obj.fetch(booking['booking_id'])
        tickets = booking_obj.get_tickets()
        refund_info['tickets'] = process_tickets(tickets)

        movie = Movie()
        movie.fetch(booking['movie_id'])
        refund_info['movie_title'] = movie.get_title()

        showtime = Showtime()
        showtime.fetch(booking['showtime_id'])
        refund_info['date'] = showtime.get_time()

        now = datetime.datetime.now()
        hour = datetime.timedelta(hours=1)
        if now + hour > showtime.get_time():
            refund_info['is_refundable'] = False
        else:
            refund_info['is_refundable'] = True


        refunds.append(dict(refund_info))

    # sort here
    refunds = sorted(refunds,
                     key=lambda k: k['date'],
                     reverse=True)
    return refunds


@bp.route('/previous_orders', methods=('GET', 'POST'))
@customer_login_required
def previous_orders():
    # need to get all booking objects for the customer
    customer = Customer()
    if not customer.fetch(g.user['username']):
        return redirect(url_for('IndexController.index'))

    if request.method == 'POST':
        refund = request.form.get('refund')
        details = request.form.get('view_details')

        if refund:
            refund_booking(refund)
            flash('Your refund request was successful. Your payment provider will be fully refunded in 3-5 days.')
        if details:
            confirm_bid = str(details) + "c"
            return redirect(url_for('BookingController.payment_confirmation', bid=confirm_bid))


    bookings = customer.get_previous_bookings()
    refunds = process_bookings(bookings)

    return render_template('orders.html', refunds=refunds)

