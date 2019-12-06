import functools

from ecinema.data.db import get_db
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

def safe_delete(movie):
    if not movie.has_showtimes():
        movie.delete(movie.get_id())
        return True
    return False


@bp.route('/manage_movies', methods=('GET', 'POST'))
@admin_login_required
def manage_movies():
    movie = Movie()

    if request.method == 'POST':
        delete_movie_id = request.form.get('delete_movie_id')
        edit_movie_id = request.form.get('edit_movie_id')

        if delete_movie_id is not None and movie.fetch(delete_movie_id):
            # logic for cancelling tickets will go here?
            if not safe_delete(movie):
                flash(
                    "Movie cannot be deleted when there are bookings for it")
        elif edit_movie_id is not None and movie.fetch(edit_movie_id):
            return redirect(
                url_for('AdminMoviesController.edit_movie', mid=edit_movie_id))

    # get a list of all movies
    movies = movie.get_all_movies()

    return render_template('manage_movies.html', movies=movies)


@bp.route('/edit_movie/<mid>', methods=('GET', 'POST'))
@admin_login_required
def edit_movie(mid):
    movie_id = mid
    movie = Movie()
    print(movie.fetch(movie_id))

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        producer = request.form.get('producer')
        cast = request.form.get('cast')
        duration = request.form.get('duration')
        synopsis = request.form.get('synopsis')
        rating = request.form.get('rating')
        category = request.form.get('category')
        video = request.form.get('video')
        picture = request.form.get('picture')

        error = None
        print(title)
        if title != '' and not validate_name(title):
            error = "Movie title is too short or too long"
        elif title != '':
            movie.set_title(title)

        if director != '' and not validate_name(director):
            error = "Director name is too short or too long"
        elif director != '':
            movie.set_director(director)

        if producer != '' and not validate_name(producer):
            error = "Producer name is too short or too long"
        elif producer != '':
            movie.set_producer(producer)

        if cast != '' and not validate_name(cast):
            error = "Cast name is too short or too long"
        elif cast != '':
            movie.set_cast(cast)

        if duration != '' and not validate_duration(duration):
            error = "Duration must be a whole number"
        elif duration != '':
            movie.set_duration(int(duration))

        if synopsis != '' and not validate_text(synopsis):
            error = "Synopsis is too long"
        elif synopsis != '':
            movie.set_synopsis(synopsis)

        if rating is not None and not validate_rating(rating):
            error = "Invalid rating"
        elif rating is not None:
            movie.set_rating(rating)

        if category is not None and not validate_category(category):
            error = "Invalid category"
        elif category is not None:
            movie.set_category(category)

        if video != '' and video.isspace():
            error = "Video link is required"
        elif video != '':
            movie.set_video(video)

        if picture != '' and picture.isspace():
            error = "Picture link is required"
        elif picture != '':
            movie.set_picture(picture)

        movie.save()

        if error is not None:
            flash(error)

    info = movie.obj_as_dict(movie_id)
    return render_template('edit_movie.html', movie=info)


@bp.route('/create_movie', methods=('GET', 'POST'))
@admin_login_required
def create_movie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        producer = request.form['producer']
        cast = request.form['cast']
        duration = request.form['duration']
        synopsis = request.form['synopsis']
        rating = request.form['rating']
        category = request.form['category']
        video = request.form['video']
        picture = request.form['picture']

        # validate all data, everything must be correct
        error = None

        db = get_db()
        if db.execute(
            'SELECT * FROM movie WHERE title = ? ',
            (title,)
        ).fetchone() is not None:
            error = "Movie already exists"
        elif not validate_name(title):
            error = "Movie title is too short or too long"
        elif not validate_name(director):
            error = "Director name is too short or too long"
        elif not validate_name(producer):
            error = "Producer name is too short or too long"
        elif not validate_name(cast):
            error = "Cast name is too short or too long"
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
                             producer=producer, cast=cast,
                             synopsis=synopsis, picture=picture,
                             video=video,
                             duration_as_minutes=int(duration),
                             rating=rating, category=category)

            # then return to add movie
            return redirect(url_for('AdminMoviesController.manage_movies'))

        flash(error)

    return render_template('make_movie.html')
