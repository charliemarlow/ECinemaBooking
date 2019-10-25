import functools

from flask import (
    Blueprint, render_template
)

bp = Blueprint('IndexController', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')

# TODO: delete all references to /index in html
# then delete this
@bp.route('/index')
def index_page():
    return render_template('index.html')
