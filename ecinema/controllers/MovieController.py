import functools

from flask import (
    Blueprint, render_template, redirect, url_for
)

from ecinema.tools.clean import create_datetime_from_sql

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from datetime import datetime

bp = Blueprint('MovieController', __name__, url_prefix='/')


@bp.route('/movie_details/<mid>')
def movie_details(mid):
    print(mid)
    movie = Movie()
    movie_dict = {}
    if movie.fetch(mid):
        movie_dict = movie.obj_as_dict(mid)
        movie_dict = dict(movie_dict)

        showtimes = movie.get_all_showtimes()
    else:
        return render_template('index.html')

    showtimes_list = []
    for showtime in showtimes:
        print(showtime['showtime_id'])
        showtime = dict(showtime)
        print(showtime['time'])
        showtime['time'] = create_datetime_from_sql(showtime['time'])
        print(showtime['time'])
        print(type(showtime['time']))
        showtimes_list.append(showtime)

    showtimes_list = sorted(showtimes_list, key=lambda k: k['time'])

    return render_template('single-product.html',
                           movie=movie_dict,
                           showtimes=showtimes_list,
                           is_current=len(showtimes) > 0)
