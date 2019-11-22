from datetime import datetime
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_name, validate_duration, validate_expiration_date
)

from ecinema.models.Promo import Promo

bp = Blueprint('AdminPromosController', __name__, url_prefix='/')

@bp.route('/manage_promos', methods=('GET', 'POST'))
@admin_login_required
def manage_promos():
    promo = Promo()

    if request.method == 'POST':
        delete_promo_id = request.form.get('delete_promo_id')
        edit_promo_id = request.form.get('edit_promo_id')

        if delete_promo_id != None and promo.fetch(delete_promo_id):
            promo.delete(delete_promo_id)
        elif edit_promo_id != None and promo.fetch(edit_promo_id):
            return redirect(url_for('AdminPromosController.edit_promo', pid=edit_promo_id))

    # get a list of all promos
    promos = promo.get_all_promos()

    return render_template('manage_promos.html', promos=promos)

@bp.route('/edit_promo/<pid>', methods=('GET', 'POST'))
@admin_login_required
def edit_promo(pid):
    promo_id = pid
    promo = Promo()
    print(promo.fetch(promo_id))

    if request.method == 'POST':

        code = request.form.get('code')
        promo_date = request.form.get('promo')

        error = None

        if code != '' and not validate_name(code):
            error = "code is invalid"
        elif code != '':
            promo.set_code(code)

        # if promo != '' and not validate_duration(promo):
        #     error = "promo is invalid"
        # elif promo != '':
        promo.set_promo(promo_date)


        if error is not None:
            flash(error)
        else:
            promo.save()
            return redirect(url_for('AdminPromosController.manage_promos'))


    info = promo.obj_as_dict(promo_id)
    return render_template('edit_promotion.html', promo=info)

@bp.route('/create_promo', methods=('GET', 'POST'))
@admin_login_required
def create_promo():
    if request.method == 'POST':

        code = request.form['code']
        promo = request.form['promo']
        # validate all data, everything must be correct
        error = None


        if not validate_name(code):
            error = "Promotion Code is invalid"
        # elif not validate_duration(promo):
        #     error = "Promotion Duration is invalid"
        

        if error is None:
            # if error is None, create a promo
            new_promo = Promo()
            new_promo.create(promo=promo,code=code)

            # then return to add promo
            return redirect(url_for('AdminPromosController.manage_promos'))

        flash(error)


    return render_template('make_promotion.html')
