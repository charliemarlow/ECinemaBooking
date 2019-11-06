
header = '''
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    {validation_list}
)

from ecinema.models.{model_class} import {model_class}

bp = Blueprint('Admin{model_plural_cap}Controller', __name__, url_prefix='/')
'''


body = '''
@bp.route('/manage_{plural_name}', methods=('GET', 'POST'))
@admin_login_required
def manage_{plural_name}():
    {lowercase_name} = {model_class}()

    if request.method == 'POST':
        delete_{lowercase_name}_id = request.form.get('delete_{lowercase_name}_id')
        edit_{lowercase_name}_id = request.form.get('edit_{lowercase_name}_id')

        if delete_{lowercase_name}_id != None and {lowercase_name}.fetch(delete_{lowercase_name}_id):
            # logic for cancelling tickets will go here?
            {lowercase_name}.delete(delete_{lowercase_name}_id)
        elif edit_{lowercase_name}_id != None and {lowercase_name}.fetch(edit_{lowercase_name}_id):
            return redirect(url_for('Admin{model_plural_cap}Controller.edit_{lowercase_name}', {id_name}=edit_{lowercase_name}_id))

    # get a list of all {lowercase_name}s
    {lowercase_name}s = {lowercase_name}.get_all_{lowercase_name}s()

    return render_template('manage_{lowercase_name}s.html', {lowercase_name}s={lowercase_name}s)

@bp.route('/edit_{lowercase_name}/<{id_name}>', methods=('GET', 'POST'))
@admin_login_required
def edit_{lowercase_name}({id_name}):
    {lowercase_name}_id = {id_name}
    {lowercase_name} = {model_class}()
    print({lowercase_name}.fetch({lowercase_name}_id))

    if request.method == 'POST':
{input_optional}

        error = None
{optional_validation}

        {lowercase_name}.save()

        if error is not None:
            flash(error)


    info = {lowercase_name}.obj_as_dict({lowercase_name}_id)
    return render_template('edit_{lowercase_name}.html', {lowercase_name}=info)

@bp.route('/create_{lowercase_name}', methods=('GET', 'POST'))
@admin_login_required
def create_{lowercase_name}():
    if request.method == 'POST':
{required_getter}
        # validate all data, everything must be correct
        error = None

{required_validation}

        if error is None:
            # if error is None, create a {lowercase_name}
            new_{lowercase_name} = {model_class}()
            new_{lowercase_name}.create({kwargs})

            # then return to add {lowercase_name}
            return redirect(url_for('Admin{model_class}sController.manage_{plural_name}'))

        flash(error)


    return render_template('make_{lowercase_name}.html')
'''

optional_getter_1 = '''
        {attr} = request.form.get('{attr}')'''

optional_validation_1 = '''
        if {attr} != '' and not {func}({attr}):
            error = "{attr} is invalid"
        elif {attr} != '':
            {class_name}.set_{attr}({attr})
'''

required_getter_template = '''
        {attr} = request.form['{attr}']'''

required_validation_1 = '''
        if not {func}({attr}):
            error = "{attr} is invalid"
'''

required_validation_2 = '''        elif not {func}({attr}):
            error = "{attr} is invalid"
'''



