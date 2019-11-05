import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_name, validate_text, validate_rating,
    validate_category, validate_duration
)

from ecinema.models.Movie import Movie

bp = Blueprint('AdminMoviesController', __name__, url_prefix='/')

@bp.route('/manage_movies', methods=('GET', 'POST'))
@admin_login_required
def manage_movies():
    movie = Movie()

    if request.method == 'POST':
        movie_id = request.form['delete_movie_id']

        if movie.fetch(movie_id):
            # logic for cancelling tickets will go here?
            movie.delete(movie_id)

    # get a list of all movies
    movies = movie.get_all_movies()

    return render_template('manage_movies.html', movies=movies)

@bp.route('/create_movie', methods=('GET', 'POST'))
@admin_login_required
def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        producer = request.form['producer']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        rating = request.form['rating']
        category = request.form['category']
        video = request.form['video']
        picture = request.form['picture']

        # validate all data, everything must be correct
        error = None

        if not validate_name(title):
            error = "Movie title is too short or too long"
        elif not validate_name(director):
            error = "Director name is too short or too long"
        elif not validate_name(producer):
            error = "Producer name is too short or too long"
        elif not validate_duration(duration):
            error = "Duration must be a whole number"
        elif not validate_text(synopsis):
            error = "Synopsis is too long"
        elif not validate_rating(rating):
            error = "Invalid rating"
        elif not validate_category(category):
            error = "Invalid category"
        elif video.isspace():
            error = "Video link is required"
        elif picture.isspace():
            error = "Picture link is required"

        if error is None:
            # if error is None, create a movie
            new_movie = Movie()
            new_movie.create(title=title, director=director,
                         producer=producer, synopsis=synopsis,
                         picture=picture, video=video, duration_as_minutes=int(duration), rating=rating, category=category)

            # then return to add movie
            return redirect(url_for('AdminMoviesController.manage_movies'))

        flash(error)


    return render_template('make_movie.html')
