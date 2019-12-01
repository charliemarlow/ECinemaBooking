
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_duration, validate_name, validate_new_seats, validate_float, validate_percentage
)
from ecinema.tools.clean import format_price

from ecinema.models.Showroom import Showroom
from ecinema.models.Showtime import Showtime
from ecinema.models.Price import Price

bp = Blueprint('AdminPriceController', __name__, url_prefix='/')


@bp.route('/edit_prices', methods=('GET', 'POST'))
@admin_login_required
def edit_prices():
    price_types = ['fees', 'tax', 'student', 'adult', 'child', 'senior']

    if request.method == 'POST':
        inputs =[]
        for typ in price_types:
            inputs.append(request.form.get(typ))
        error = None

        for i, inp in enumerate(inputs):

            if price_types[i] == 'tax' and inp and validate_percentage(inp):
                price = Price()
                price.fetch(price_types[i])
                price.set_price(float(inp))
                price.save()
                continue
            elif price_types[i] == 'tax' and inp:
                error = "Invalid percentage, you must enter a valid percentage"
                continue


            if inp and validate_float(inp):
                price = Price()
                price.fetch(price_types[i])
                price.set_price(float(inp))
                price.save()
            elif not validate_float(inp):
                error = "Invalid price, you must enter a valid number"
        if error is not None:
            flash(error)


    price_dicts = []
    price_d = {}
    for p in price_types:
        price = Price()
        price.fetch(p)

        price_d['name'] = p
        price_d['price'] = price.get_price()
        price_dicts.append(dict(price_d))

    return render_template('edit_prices.html', prices=price_dicts)
