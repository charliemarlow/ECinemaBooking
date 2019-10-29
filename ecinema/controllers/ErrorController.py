from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)

bp = Blueprint('ErrorController', __name__, url_prefix='/')

app = Flask(__name__)

