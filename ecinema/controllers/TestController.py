import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
bp = Blueprint('TestController', __name__, url_prefix='/')


@bp.route('/orders', methods=('GET', 'POST'))
def manage_payment():
    return render_template('orders.html')

