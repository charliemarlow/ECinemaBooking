import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)

from ecinema.models.Movie import Movie
from ecinema.tools.clean import create_datetime_from_sql

from ecinema.data.db import get_db
from datetime import datetime
import pdb

bp = Blueprint('SearchController', __name__, url_prefix='/')


@bp.route('/search', methods=('GET', 'POST'))
def search():

    movie = Movie()

    sinput = ''
    dinput = ''
    catinput = ''
    search_args = []

    if request.method == 'POST':
        search_input = request.form.get('search_input')
        category = request.form.get('category')
        date = request.form.get('date')

        if search_input != '' and search_input is not None:
            sinput = search_input
            search_args.append('title LIKE "%{}%"'.format(search_input))

        if category != '' and category is not None:
            search_args.append('category = "{}"'.format(category))
            catinput = category.title()

        if date != '' and date is not None:
            search_args.append('date(time) = "{}"'.format(date))
            dinput = date

        db = get_db()

        # handle search args being none
        first = True
        sql = 'SELECT movie.movie_id, title, category, picture, video, rating, status, time FROM movie NATURAL JOIN showtime WHERE '
        farg = ''
        for arg in search_args:
            if first:
                farg = sql + arg
                first = False
            else:
                farg = farg + " AND " + arg

        print(farg)
        movies = db.execute(farg).fetchall()

        if len(movies) > 0:
            curr_id = movies[0]['movie_id']
            curr_movie = []
            show_movies = []

            nmovies = sorted(movies, key=lambda k: k['time'])

            for mov in nmovies:
                mov = dict(mov)
                mov['time'] = create_datetime_from_sql(mov['time'])
                if curr_id != mov['movie_id']:
                    show_movies.append(list(curr_movie))
                    curr_id = mov['movie_id']
                    curr_movie.clear()

                curr_movie.append(mov)

            show_movies.append(curr_movie)
        else:
            if search_input == '' and category is None and date == '':
                flash("At least one search field must be filled")
            else:
                flash("No movies found :(")
            show_movies = None


    return render_template('search.html',
                           movies=show_movies,
                           search_input=sinput,
                           date_input=dinput,
                           category_in=catinput)

def search_keyword(word):
    pass
