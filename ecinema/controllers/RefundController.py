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

def refund(bid):
    # clean up
    # delete all tickets, reset showtime incrementer
    # delete the booking object
    return

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
            print("Refund = " + refund)
        if details:
            print("details = " + details)



    # then fill this out
    refund_info = {
        'movie_title' : 'test',
        'order_no' : '#AF13J',
        'date' : datetime.datetime.now(),
        'tickets' : '2 x Adults, 1 x Child',
        'total' : '$19.36 USD',
        'bid' : 0, # or None if no longer available
    }
    refunds = []
    refunds.append(refund_info)
    flash('Your refund request was successful. Your payment provider will be fully refunded in 3-5 days.')
    return render_template('orders.html', refunds=refunds)

