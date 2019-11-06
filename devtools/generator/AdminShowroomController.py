
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_showtime_date, validate_seats, validate_movie, validate_showroom
)

from ecinema.models.Showroom import Showroom

bp = Blueprint('AdminShowroomsController', __name__, url_prefix='/')

@bp.route('/manage_showrooms', methods=('GET', 'POST'))
@admin_login_required
def manage_showrooms():
    showroom = Showroom()

    if request.method == 'POST':
        delete_showroom_id = request.form.get('delete_showroom_id')
        edit_showroom_id = request.form.get('edit_showroom_id')

        if delete_showroom_id != None and showroom.fetch(delete_showroom_id):
            # logic for cancelling tickets will go here?
            showroom.delete(delete_showroom_id)
        elif edit_showroom_id != None and showroom.fetch(edit_showroom_id):
            return redirect(url_for('AdminShowroomsController.edit_showroom', sid=edit_showroom_id))

    # get a list of all showrooms
    showrooms = showroom.get_all_showrooms()

    return render_template('manage_showrooms.html', showrooms=showrooms)

@bp.route('/edit_showroom/<sid>', methods=('GET', 'POST'))
@admin_login_required
def edit_showroom(sid):
    showroom_id = sid
    showroom = Showroom()
    print(showroom.fetch(showroom_id))

    if request.method == 'POST':

        time = request.form.get('time')
        available_seats = request.form.get('available_seats')
        movie_id = request.form.get('movie_id')
        showroom_id = request.form.get('showroom_id')

        error = None

        if time != '' and not validate_showtime_date(time):
            error = "time is invalid"
        elif time != '':
            showroom.set_time(time)

        if available_seats != '' and not validate_seats(available_seats):
            error = "available_seats is invalid"
        elif available_seats != '':
            showroom.set_available_seats(available_seats)

        if movie_id != '' and not validate_movie(movie_id):
            error = "movie_id is invalid"
        elif movie_id != '':
            showroom.set_movie_id(movie_id)

        if showroom_id != '' and not validate_showroom(showroom_id):
            error = "showroom_id is invalid"
        elif showroom_id != '':
            showroom.set_showroom_id(showroom_id)


        showroom.save()

        if error is not None:
            flash(error)


    info = showroom.obj_as_dict(showroom_id)
    return render_template('edit_showroom.html', showroom=info)

@bp.route('/create_showroom', methods=('GET', 'POST'))
@admin_login_required
def create_showroom():
    if request.method == 'POST':

        time = request.form['time']
        available_seats = request.form['available_seats']
        movie_id = request.form['movie_id']
        showroom_id = request.form['showroom_id']
        # validate all data, everything must be correct
        error = None


        if not validate_showtime_date(time):
            error = "time is invalid"
        elif not validate_seats(available_seats):
            error = "available_seats is invalid"
        elif not validate_movie(movie_id):
            error = "movie_id is invalid"
        elif not validate_showroom(showroom_id):
            error = "showroom_id is invalid"


        if error is None:
            # if error is None, create a showroom
            new_showroom = Showroom()
            new_showroom.create(showroom_id=showroom_id)

            # then return to add showroom
            return redirect(url_for('AdminShowroomsController.manage_showrooms'))

        flash(error)


    return render_template('make_showroom.html')
