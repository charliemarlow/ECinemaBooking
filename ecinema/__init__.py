import os

from flask import Flask


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
    from ecinema.controllers import RegisterController
    from ecinema.controllers import LoginController
    from ecinema.controllers import IndexController
    from ecinema.controllers import AccountController
    from ecinema.controllers import ResetPasswordController
    from ecinema.controllers import TestController
    from ecinema.controllers import ForgotPasswordController

    app.register_blueprint(RegisterController.bp)
    app.register_blueprint(LoginController.bp)
    app.register_blueprint(IndexController.bp)
    app.register_blueprint(AccountController.bp)
    app.register_blueprint(ResetPasswordController.bp)
    app.register_blueprint(ForgotPasswordController.bp)

    return app
