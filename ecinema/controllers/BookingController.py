import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session, current_app, Flask
)
import datetime

from ecinema.tools.clean import create_datetime_from_sql, clean_tickets
from ecinema.tools.validation import validate_name, validate_duration, validate_text

from ecinema.controllers.LoginController import customer_login_required
from apscheduler.schedulers.background import BackgroundScheduler

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Showroom import Showroom
from ecinema.models.Review import Review
from ecinema.models.Customer import Customer
from ecinema.models.Price import Price
from ecinema.models.Ticket import Ticket

bp = Blueprint('BookingController', __name__, url_prefix='/')

'''
def clear_tickets(session):
    print("requesting context")
    app = Flask(__name__)
    app.app_context().push()
    with app.app_context():
        with current_app.app_context():
            print("in clear tickets")
            if session.get('tickets') and session.get('ticket_ids'):
                print("sessionion gotem")
                ticket = Ticket()
                del session['tickets']
                ticket = ticket.fetch(session['ticket_ids'][0])

                showtime = Showtime()
                showtime.fetch(ticket.get_showtime_id())

                new_available = showtime.get_available_seats() + len(session['tickets'])
                showtime.set_available_seats(new_available)
                showtime.save()

                for tid in session['ticket_ids']:
                    ticket.delete(tid)

                del session['ticket_ids']

def reserve_tickets(showtime):
    with current_app.app_context():
        print("success")

    new_available = showtime.get_available_seats() - len(session['tickets'])
    showtime.set_available_seats(new_available)
    showtime.save()

    showtime_id = showtime.get_id()
    session['ticket_ids'] = []

    for ticket_tuple in session['tickets']:
        ticket = Ticket()
        ticket.create(showtime_id=showtime_id,
                      booking_id=None,
                      age=ticket_tuple[1],
                      seat_number=ticket_tuple[0])
        session['ticket_ids'].append(ticket.get_id())

    scheduler = BackgroundScheduler()
    one_hour = datetime.datetime.now() + datetime.timedelta(seconds=1)
    scheduler.add_job(func=lambda: clear_tickets(session), trigger="date", run_date=one_hour)
    scheduler.start()


@bp.route('/confirm_booking', methods=('GET', 'POST'))
@customer_login_required
def confirm_booking():

    if not session.get('tickets') or not session.get('showtime'):
        return redirect(url_for('IndexController.index'))

    showtime = Showtime()
    showtime.fetch(session['showtime'])

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
        elif request.form.get('proceed'):
            print("proceeding")
            # reserve_tickets(showtime)
            return redirect(url_for('CheckoutController.checkout'))
        # need to add logic for going to the next page
        # it should hold the tickets, and start a checkout timer
        # reserving means reducing the showtimes available seats
        # and creating tickets for those seats with a null booking id
        # if time passes, we reset the available seats
        # and

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

'''


@bp.route('/cancel_booking', methods=('GET', 'POST'))
@customer_login_required
def cancel_booking():
    return render_template("bookingfail.html")


@bp.route('/payment_confirmation', methods=('GET', 'POST'))
@customer_login_required
def payment_confirmation():
    return render_template('confirmation.html')
