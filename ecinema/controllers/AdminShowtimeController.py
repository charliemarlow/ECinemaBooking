
import functools
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_seats
)

from ecinema.models.Showtime import Showtime
from ecinema.models.Movie import Movie
from ecinema.models.Showroom import Showroom
from ecinema.tools.clean import create_datetime_from_sql

bp = Blueprint('AdminShowtimeController', __name__, url_prefix='/')

def safe_delete(showtime):
    if not showtime.has_tickets() and not showtime.has_bookings():
        showtime.delete(showtime.get_id())
        return True
    return False

@bp.route('/manage_showtime', methods=('GET', 'POST'))
@admin_login_required
def manage_showtime():
    showtime = Showtime()

    if request.method == 'POST':
        delete_showtime_id = request.form.get('delete_showtime_id')
        edit_showtime_id = request.form.get('edit_showtime_id')

        if delete_showtime_id is not None and showtime.fetch(
                delete_showtime_id):
            # logic for cancelling tickets will go here?
            if not safe_delete(showtime):
                flash("Cannot delete showtime, it has associated bookings")
        elif edit_showtime_id is not None and showtime.fetch(edit_showtime_id):
            return redirect(
                url_for('AdminShowtimeController.edit_showtime', sid=edit_showtime_id))

    # get a list of all showtimes
    showtimes = showtime.get_all_showtimes()
    new_times = []

    for time in showtimes:
        time = dict(time)
        movie = Movie()
        movie.fetch(time['movie_id'])

        showroom = Showroom()
        showroom.fetch(time['showroom_id'])

        time['time'] = create_datetime_from_sql(time['time'])
        time['movie_title'] = movie.get_title()
        time['duration'] = movie.get_duration()
        time['showroom_name'] = showroom.get_showroom_name()

        new_times.append(time)

    # show newest times first
    new_times = sorted(new_times, key=lambda k: k['time'])

    return render_template('manage_showtime.html', showtimes=new_times)


@bp.route('/edit_showtime/<sid>', methods=('GET', 'POST'))
@admin_login_required
def edit_showtime(sid):
    showtime_id = sid
    showtime = Showtime()
    if not showtime.fetch(showtime_id):
        print("Error fetching showtime??")

    movie = Movie()
    movies = movie.get_all_movies()
    movie.fetch(showtime.get_movie_id())
    showroom = Showroom()
    showrooms = showroom.get_all_showrooms()
    showroom.fetch(showtime.get_showroom_id())

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        available_seats = request.form.get('available_seats')
        movie_id = request.form.get('movie_id')
        showroom_id = request.form.get('showroom_id')

        print(date)
        print(time)
        print(available_seats)
        print(movie_id)
        print(showroom_id)
        error = None

        dtime = create_datetime(date, time)

        if not validate_showtime_date(dtime):
            error = "The selected showroom is unavailable at that time"
        elif not validate_showroom_availability(showroom.get_id(), showtime_id, dtime, int(movie.get_duration())):
            error = "The selected showroom is unavailable at that time"
        else:
            showtime.set_time(dtime)

        if movie_id is not None and not validate_movie(movie_id):
            error = "There was an error processing the movie"
        elif movie_id is not None:
            showtime.set_movie_id(movie_id)

        if showroom_id is not None and not validate_showroom(showroom_id):
            error = "There was an error processing the showroom"
        elif showroom_id is not None:
            showtime.set_showroom_id(showroom_id)

        showtime.save()

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('AdminShowtimeController.manage_showtime'))

    info = showtime.obj_as_dict(showtime_id)
    print("show_dtime")
    print(info['time'])
    show_dtime = create_datetime_from_sql(info['time'])
    return render_template('edit_showtime.html',
                           showtime=info,
                           movie_title=movie.get_title(),
                           showroom_name=showroom.get_showroom_name(),
                           show_dtime=show_dtime,
                           movies=movies,
                           showrooms=showrooms)


def create_datetime(date, time):
    try:
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])

        hour = int(time[0:2])
        minute = int(time[3:5])

        return datetime(year, month, day, hour, minute, 00)
    except ValueError:
        return None


def validate_showtime_date(date):
    # check that showtime is later than today
    return date > datetime.now()


def validate_movie(movie_id):
    movie = Movie()
    return movie.fetch(movie_id)


def validate_showroom_availability(showroom_id, showtime_id, time, duration):
    showroom = Showroom()
    if showroom.fetch(showroom_id):
        return showroom.check_availability(time, showtime_id, duration)

    return False


@bp.route('/create_showtime', methods=('GET', 'POST'))
@admin_login_required
def create_showtime():
    movie = Movie()
    movies = movie.get_all_movies()
    showroom = Showroom()
    showrooms = showroom.get_all_showrooms()

    if request.method == 'POST':

        date = request.form['date']
        time = request.form['time']
        movie_id = request.form['movie_id']
        showroom_id = request.form['showroom_id']

        # validate all data, everything must be correct
        error = None

        movie = Movie()
        validate_movie = movie.fetch(movie_id)

        # convert date and time into a datetime object
        dtime = create_datetime(date, time)

        if dtime is None:
            error = "Time is invalid"
        elif not validate_showtime_date(dtime):
            error = "Time is in the past"
        elif not validate_movie:
            error = "The selected movie is invalid"
        elif not validate_showroom_availability(showroom_id, 0, dtime, int(movie.get_duration())):
            error = "The showroom is unavailable at that time"

        if error is None:
            # if error is None, create a showtime
            new_showtime = Showtime()
            showroom = Showroom()
            showroom.fetch(showroom_id)
            movie.set_status('active')
            movie.save()

            new_showtime.create(showroom_id=showroom_id,
                                time=dtime,
                                movie_id=movie_id,
                                available_seats=showroom.get_num_seats())

            # then return to add showtime
            return redirect(url_for('AdminShowtimeController.manage_showtime'))

        flash(error)

    return render_template('make_showtime.html',
                           movies=movies, showrooms=showrooms)
