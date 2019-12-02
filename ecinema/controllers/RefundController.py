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
from ecinema.models.UserFactory import create_user
from ecinema.models.Price import Price
from ecinema.models.Ticket import Ticket
from ecinema.models.Booking import Booking

bp = Blueprint('RefundController', __name__, url_prefix='/')

def delete_booking_and_tickets(bid):
    booking = Booking()
    booking.fetch(bid)

    tickets = booking.get_tickets()
    ticket_obj = Ticket()
    for ticket in tickets:
        ticket_obj.delete(ticket['ticket_id'])

    booking.delete(bid)

def refund_booking(bid):
    # clean up
    # delete all tickets, reset showtime incrementer
    booking = Booking()
    if not booking.fetch(bid):
        return redirect(url_for('IndexController.index'))
    total = booking.get_total_price()

    movie = Movie()
    movie.fetch(booking.get_movie_id())
    movie_title = movie.get_title()

    tickets = booking.get_tickets()
    ticket_count = len(tickets)

    # delete individual ticket objects
    ticket_obj = Ticket()
    for ticket in tickets:
        ticket_obj.delete(ticket['ticket_id'])

    # delete the actual booking object
    showtime = booking.get_showtime_id()
    booking.delete(bid)

    # reset showtime seats
    showtime_obj = Showtime()
    showtime_obj.fetch(showtime)
    showtime_obj.increment_available_seats(ticket_count)
    time = showtime_obj.get_time().strftime('%I:%M %p  :  %B %d, %Y')
    showtime_obj.save()

    # send an email!
    customer = create_user('customer')
    customer.fetch(g.user['username'])
    customer.send_refund_email(movie_title, time, format_price(total))

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
        print(showtime.fetch(booking['showtime_id']))
        print(booking['showtime_id'])
        refund_info['date'] = showtime.get_time()
        print(showtime.get_time())

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
    customer = create_user('customer')
    if not customer.fetch(g.user['username']):
        return redirect(url_for('IndexController.index'))

    if request.method == 'POST':
        refund = request.form.get('refund')
        details = request.form.get('view_details')

        if refund:
            refund_booking(refund)
            flash('Your refund request was successful. Your payment card will be fully refunded in 3-5 days.')
        if details:
            confirm_bid = str(details) + "c"
            return redirect(url_for('BookingController.payment_confirmation', bid=confirm_bid))


    bookings = customer.get_previous_bookings()
    refunds = process_bookings(bookings)

    refunds = sorted(refunds, key=lambda k : k['date'])
    return render_template('orders.html', refunds=refunds)

