
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_duration, validate_name, validate_new_seats
)

from ecinema.models.Showroom import Showroom
from ecinema.models.Showtime import Showtime

bp = Blueprint('AdminShowroomController', __name__, url_prefix='/')


@bp.route('/manage_showrooms', methods=('GET', 'POST'))
@admin_login_required
def manage_showrooms():
    showroom = Showroom()

    if request.method == 'POST':
        delete_showroom_id = request.form.get('delete_showroom_id')
        edit_showroom_id = request.form.get('edit_showroom_id')

        if delete_showroom_id is not None and showroom.fetch(
                delete_showroom_id):
            # need to make sure there are no showtimes first
            if not showroom.has_showtimes():
                showroom.delete(delete_showroom_id)
            else:
                flash(
                    "Showroom cannot be removed when there are showtimes associated with it")
        elif edit_showroom_id is not None and showroom.fetch(edit_showroom_id):
            return redirect(url_for('AdminShowroomController.edit_showroom',
                                    sid=edit_showroom_id))

    # get a list of all showrooms
    showrooms = showroom.get_all_showrooms()

    return render_template('manage_showrooms.html',
                           showrooms=showrooms)


@bp.route('/edit_showroom/<sid>', methods=('GET', 'POST'))
@admin_login_required
def edit_showroom(sid):
    showroom_id = sid
    showroom = Showroom()
    print(showroom.fetch(showroom_id))

    if request.method == 'POST':
        print("posted")

        num_seats = request.form.get('num_seats')
        showroom_name = request.form.get('showroom_name')

        error = None

        if num_seats != '' and not validate_duration(num_seats):
            error = "Capacity must be a whole number"
            print("setting error")
        elif validate_duration(num_seats) and int(num_seats) <= 0:
            error = "Number of seats must be a positive, non-zero whole number"
        elif num_seats != '':
            if showroom.update_num_seats(num_seats):
                showroom.set_num_seats(num_seats)
            else:
                error = "Too many seats are booked to reduce the number of seats at this time, wait for the showtimes to pass before changing the number of seats"

        if showroom_name != '' and not validate_name(showroom_name):
            error = "Showroom name is invalid"
        elif showroom_name != '':
            showroom.set_showroom_name(showroom_name)

        showroom.save()

        if error is not None:
            print("flashing :" + error)
            flash(error)
        else:
            return redirect(
                url_for('AdminShowroomController.manage_showrooms'))

    info = showroom.obj_as_dict(showroom_id)
    return render_template('edit_hall.html', showroom=info)


def unique_showroom(name: str):
    showroom = Showroom()
    return showroom.unique_name(name)


@bp.route('/create_showroom', methods=('GET', 'POST'))
@admin_login_required
def create_showroom():
    if request.method == 'POST':

        num_seats = request.form['num_seats']
        showroom_name = request.form['showroom_name']
        # validate all data, everything must be correct
        error = None

        if not validate_duration(num_seats):
            error = "Number of seats must be a positive, non-zero whole number"
        elif validate_duration(num_seats) and int(num_seats) <= 0:
            error = "Number of seats must be a positive, non-zero whole number"
        elif not validate_name(showroom_name):
            error = "Showroom name is invalid"
        elif not unique_showroom(showroom_name):
            error = "Showroom name must be unique"

        if error is None:
            # if error is None, create a showroom
            new_showroom = Showroom()
            new_showroom.create(showroom_name=showroom_name,
                                num_seats=num_seats, theater_id="1")

            # then return to add showroom
            return redirect(
                url_for('AdminShowroomController.manage_showrooms'))

        flash(error)

    return render_template('make_hall.html')
