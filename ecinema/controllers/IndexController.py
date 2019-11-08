import functools

from flask import (
    Blueprint, render_template, redirect, url_for
)

from ecinema.models.Movie import Movie

bp = Blueprint('IndexController', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    movie = Movie()
    current_movies = movie.get_current_movies()
    coming_soon = movie.get_coming_movies()

    return render_template('index.html',
                           current_movies=current_movies,
                           coming_movies=coming_soon)

# TODO: delete all references to /index in html
# then delete this
@bp.route('/index')
def index_page():
    return redirect(url_for('IndexController.index'))
