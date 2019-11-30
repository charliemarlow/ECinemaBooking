import functools

from flask import (
    Blueprint, render_template, redirect, url_for, request, g, flash,
    session
)
from datetime import datetime

from ecinema.tools.clean import create_datetime_from_sql
from ecinema.tools.validation import validate_name, validate_duration, validate_text, validate_showtime

from ecinema.controllers.LoginController import customer_login_required
from ecinema.models.UserFactory import create_user

from ecinema.models.Movie import Movie
from ecinema.models.Showtime import Showtime
from ecinema.models.Review import Review

from ecinema.tools.data_integrity import clear_all_booking

bp = Blueprint('MovieController', __name__, url_prefix='/')


@bp.route('/movie_details/<mid>', methods=('GET', 'POST'))
def movie_details(mid):
    print(mid)

    clear_all_booking()

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
        showtime = dict(showtime)
        showtime['time'] = create_datetime_from_sql(showtime['time'])
        if validate_showtime(showtime['available_seats'], showtime['time']):
            showtimes_list.append(showtime)

    showtimes_list = sorted(showtimes_list, key=lambda k: k['time'])

    # for each review
    review_model = Review()

    if request.method == 'POST':
        review_id = request.form.get('review_id')
        if review_id != '':
            review_model.delete(review_id)

        showtime_id = request.form.get('showtime')
        if showtime_id != '':
            session['showtime'] = showtime_id
            print("showtime")
            print(showtime_id)
            return redirect(url_for('SeatSelectionController.select_seat'))

    reviews = review_model.get_all_reviews_by_movie(mid)
    display_reviews = []
    if len(reviews) > 0:
        for review in reviews:
            rvw = dict(review)
            rvw['name'] = review_model.get_customer_name(rvw['customer_id'])
            print(rvw['name'])
            display_reviews.append(rvw)
    else:
        rev = {
            'title': "There's no reviews yet?",
            'name': "E-Cinema Booking Team",
            'rating': 5,
            'review': "There are no reviews for this movie yet. You can click on the review movie button below to be the first!"
        }
        display_reviews.append(rev)

    return render_template('single-product.html',
                           movie=movie_dict,
                           showtimes=showtimes_list,
                           is_current=len(showtimes) > 0,
                           reviews=display_reviews)


# create review should be a separate screen
# pass the mid in as a parameter
@bp.route('/create_review/<mid>', methods=('GET', 'POST'))
@customer_login_required
def create_review(mid):
    # tell them what movie it is for
    movie = Movie()
    movie = movie.obj_as_dict(mid)

    if request.method == 'POST':
        rating = request.form['rating']
        title = request.form['title']
        review = request.form['review']

        error = None
        if not validate_duration(rating):
            error = "Rating is invalid"
        elif not validate_name(title):
            error = "Title is invalid"
        elif not validate_text(review):
            error = "Review is invalid"

        if error is None:
            # write it to the db
            customer = create_user('customer')
            # customer login required ensures this will work
            customer.fetch(g.user['username'])
            review_model = Review()
            review_model.create(customer_id=customer.get_id(),
                                movie_id=movie['movie_id'],
                                rating=int(rating),
                                subject=title,
                                review=review)

            return redirect(
                url_for('MovieController.movie_details', mid=movie['movie_id']))

        flash(error)

    return render_template('create_review.html',
                           movie=movie)
