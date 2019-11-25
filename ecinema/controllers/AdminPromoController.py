from datetime import datetime
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_name, validate_expiration_date, validate_promo_code, validate_unlinked_promo
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
            if validate_unlinked_promo(delete_promo_id):
                promo.delete(delete_promo_id)
            else:
                error = "Promo is linked to a booking. Cannot delete right now"
                flash(error)
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
        promo_description = request.form.get('description')

        promo_date_dict = promo_date.split("-")
        date = datetime(int(promo_date_dict[0]), int(promo_date_dict[1]), int(promo_date_dict[2]))

        error = None

        if code != '' and not validate_name(code):
            error = "Promotion Code is invalid"
        elif code !='' and not validate_promo_code(code):
            error = "Promotion Code already exists"
        elif code != '':
            promo.set_code(code)

        if promo != '' and not validate_expiration_date(date):
            error = "Promotion Valid Until Date is invalid"
        elif promo != '':
            promo.set_promo(promo_date)
        promo.set_description(promo_description)


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
        description = request.form.get('description')
        # validate all data, everything must be correct
        error = None
        promo_date = promo.split("-")
        date = datetime(int(promo_date[0]), int(promo_date[1]), int(promo_date[2]))


        if not validate_name(code):
            error = "Promotion Code is invalid"
        elif not validate_promo_code(code):
            error = "Promotion Code already exists"
        elif not validate_expiration_date(date):
            error = "Promotion Valid Until Date is invalid"
        

        if error is None:
            # if error is None, create a promo
            new_promo = Promo()
            new_promo.create(promo=promo,code=code,description=description)

            # then return to add promo
            return redirect(url_for('AdminPromosController.manage_promos'))

        flash(error)


    return render_template('make_promotion.html')
