import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)

from ecinema.models.Search import Search
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

        search = Search()
        sinput = search_input
        search.set_term(search_input)

        if category is not None:
            search.set_category(category)
            catinput = category.title()

        dinput = date
        search.set_date(date)

        # execute a search
        movies, error = search.execute()

        if error is not None and error != "COMINGSOON":
            flash(error)

    return render_template('search.html',
                           movies=movies,
                           search_input=sinput,
                           date_input=dinput,
                           category_in=catinput)
