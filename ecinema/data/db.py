import sqlite3
from werkzeug.security import generate_password_hash
import click
from flask import current_app, g
from flask.cli import with_appcontext

schema_list = ["schema/address.sql",
               "schema/customer.sql",
               "schema/credit_card.sql",
               "schema/admin.sql",
               "schema/movie.sql",
               "schema/theater.sql",
               "schema/showroom.sql",
               "schema/showtime.sql",
               "schema/review.sql",
               "schema/booking.sql",
               "schema/ticket.sql",
               "schema/promo.sql",
               "schema/price.sql"]

def init_db():
    db = get_db()

    for sqlFile in schema_list:
        print(sqlFile)
        with current_app.open_resource(sqlFile) as f:
            db.executescript(f.read().decode('utf8'))


    db.execute(
        'INSERT INTO admin (username, password) VALUES (?, ?)',
        ("admin", generate_password_hash("Password123")),
    )
    db.execute(
        'INSERT INTO theater (name) VALUES (?)',
        ("E-Cinema",)
    )

    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("init db")


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
