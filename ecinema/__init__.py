import os

from flask import Flask, render_template
from ecinema.controllers import (
    RegisterController, LoginController, IndexController,
    AccountController, ResetPasswordController,
    TestController, ForgotPasswordController
)


def not_found(e):
    return render_template('error.html'), 404


def create_app(test_config=None):
    # set up flask
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ecinema.sqlite')
    )

    # load configs
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # set up database
    from ecinema.data import db
    db.init_app(app)

    # load Page Controllers
    app.register_blueprint(RegisterController.bp)
    app.register_blueprint(LoginController.bp)
    app.register_blueprint(IndexController.bp)
    app.register_blueprint(AccountController.bp)
    app.register_blueprint(ResetPasswordController.bp)
    app.register_blueprint(ForgotPasswordController.bp)

    # load error handlers
    app.register_error_handler(404, not_found)

    return app
