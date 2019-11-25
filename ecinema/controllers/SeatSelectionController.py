import functools
import json

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
from ecinema.models.Ticket import Ticket

bp = Blueprint('SeatSelectionController', __name__, url_prefix='/')


def reserve_tickets(showtime):

    reset_available_seats()

    ticket_len = 0
    if session.get('tickets'):
        ticket_len = len(session['tickets'])

    # set showtime availability
    new_available = showtime.get_available_seats() - ticket_len
    showtime.set_available_seats(new_available)
    showtime.save()

    # need to reserve tickets here
    clear_ticket_ids()

    ticket = Ticket()
    showtime_id = showtime.get_id()

    if ticket_len != 0:
        session['ticket_ids'] = []
        for ticket_tuple in session['tickets']:
            ticket.create(showtime_id=showtime_id,
                          booking_id=None,
                          age=ticket_tuple[1],
                          seat_number=ticket_tuple[0])
            session['ticket_ids'].append(ticket.get_id())


def reset_available_seats():
    if not session.get('showtime'):
        print("Error resetting available seats")

    if not session.get('ticket_ids'):
        return

    showtime = Showtime()
    showtime.fetch(session['showtime'])

    reset_len = len(session['ticket_ids'])
    avail = showtime.get_available_seats()
    new_avail = avail + reset_len
    showtime.set_available_seats(new_avail)
    showtime.save()


def clear_ticket_ids():
    ticket = Ticket()

    if session.get('ticket_ids'):
        for tid in session['ticket_ids']:
            ticket.delete(tid)
        del session['ticket_ids']


@bp.route('/select_seat', methods=('GET', 'POST'))
@customer_login_required
def select_seat():

    if not session.get('showtime') or not g.user.get('username'):
        return redirect(url_for('IndexController.index'))

    # INFO we need: showtime_id and customer
    showtime = Showtime()
    showtime.fetch(session['showtime'])

    if request.method == 'POST':
        reserve_tickets(showtime)
        return redirect(url_for('CheckoutController.checkout'))

    showroom = Showroom()
    showroom.fetch(showtime.get_showroom_id())

    tickets = showtime.get_all_tickets()

    # probably need to pull all tickets
    # for this showtime, and get a list of taken
    # seats to pass to zach
    available = list(range(13))
    if len(tickets) > 0:
        for ticket in tickets:
            seat_no = int(ticket['seat_number'])
            available[seat_no] = -1

    avail_dict = {'capacity': showroom.get_num_seats(),
                  'row': 8,
                  'seats': available
                  }

    # ZACH:
    # from this page, we'll get the seats and their ages
    # we need to get an array of tuples like
    # [(seatNo, age),]
    example = [(12, "adult"), (11, "student")]
    print(session.get('tickets'))
    if session.get('tickets') is not None:
        session['tickets'] = session['tickets'] + example
    else:
        session['tickets'] = example

    return render_template("seat_selection.html", tickets=avail_dict)
