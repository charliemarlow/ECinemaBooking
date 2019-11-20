import functools
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash

from ecinema.models.Customer import Customer
from ecinema.models.Address import Address
from ecinema.models.CreditCard import CreditCard

from ecinema.controllers.LoginController import (
    login_required, verify_username_password, get_user
)

from ecinema.tools.validation import (
    validate_name, validate_email, validate_unique_email,
    validate_cvv, validate_cc_number, validate_expiration_date,
    validate_zip, validate_state, validate_phone, validate_year
)
from ecinema.tools.clean import clean_phone, clean_expiration

bp = Blueprint('AccountController', __name__, url_prefix='/')


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    return render_template('account.html')


@bp.route('/editprofile', methods=('GET', 'POST'))
@login_required
def edit_profile():
    customer = Customer()
    addr = Address()

    user_id = session.get('user_id')
    customer.fetch(user_id)

    if customer.get_address_id() is not None:
        addr.fetch(customer.get_address_id())
    info_changed = False

    if(not customer.fetch(user_id)):
        return render_template("index.html")

    if request.method == 'POST':
        first_name = request.form.get('first')
        last_name = request.form.get('last')
        phone = request.form.get('phone')
        subscribe = request.form.get('subscribe') is not None

        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        error = None
        if first_name != '':
            if validate_name(first_name):
                customer.set_first_name(first_name)
                info_changed = True
            else:
                error = "Invalid name"

        if last_name != '':
            if validate_name(last_name):
                customer.set_last_name(last_name)
                info_changed = True
            else:
                error = "Invalid name"

        if phone != '' and phone is not None:
            if validate_phone(phone):
                customer.set_phone(clean_phone(phone))
                info_changed = True
            else:
                error = "Invalid phone number"

        if customer.get_promo() is not subscribe:
            if customer.get_promo() != subscribe:
                info_changed = True
            customer.set_promo(subscribe)

        if not customer.save():
            error = error + "Issue saving customer details"
            info_changed = False

        # either create, or save addr here
        # get address ID from customer

        addr_id = customer.get_address_id()
        print("addr_id")
        print(addr_id)
        if addr_id is None:
            if (street != '' and city != '' and
                state != '' and zip_code != ''):
                addr_error = None
                if not validate_zip(zip_code):
                    addr_error = 'Zip code must be a valid zip code and '\
                        + 'be entered in ##### or #####-#### format'
                elif not validate_state(state):
                    addr_error = 'State must be valid and entered in ## format'

                print("About to Create")
                if addr_error is None:
                    addr.create(street=street, city=city,
                                state=state, zip_code=zip_code)
                    customer.set_address_id(addr.get_id())
                    customer.save()
                    info_changed = True
                else:
                    error = addr_error
            else:
                error = "To create a home address, all address information is required with zip code in #####-#### format and state in ## format"
        else:
            print("about to fetch addr")
            print(addr.fetch(addr_id))

            if street != '':
                print("street")
                print(street)
                addr.set_street(street)
                info_changed = True

            if city != '':
                addr.set_city(city)
                info_changed = True

            if state != '':
                if validate_state(state):
                    addr.set_state(state)
                    info_changed = True
                else:
                    error = 'State must be valid USA state '\
                        + 'in ## format (example, GA)'

            if zip_code != '':
                if validate_zip(zip_code):
                    addr.set_zip(zip_code)
                    print("setting ZIP code")
                    info_changed = True
                else:
                    error = 'Zip code must be a valid USA zip code'\
                        + ' in ##### or #####-#### format'

            print("About to save")
            addr.save()

        if error is not None:
            flash(error)

        if info_changed:
            customer.send_profile_change_email()

    address = addr.obj_as_dict(addr.get_id())
    if not address:
        address = {
            'state': 'State (Required)',
            'city': 'City (Required)',
            'street': 'Street (Required)',
            'zip_code': 'ZIP Code (Required)'
        }
    user = customer.obj_as_dict(user_id)
    return render_template('editprofile.html', user=user, address=address)


@bp.route('/manage_payment', methods=('GET', 'POST'))
@login_required
def manage_payment():
    # call customer object to return a list of all
    # credit cards
    customer = Customer()
    fetched = customer.fetch(session['user_id'])

    if request.method == 'POST':
        card_id = request.form.get('cid')
        edit_id = request.form.get('edit_cid')
        card = CreditCard()
        if card_id != '' and card.fetch(card_id):
            card.delete(card_id)
            customer.send_delete_card_email()
        elif edit_id != '':
            print(edit_id)
            return redirect(url_for('AccountController.edit_payment', cid=edit_id))

    if fetched:
        print(customer.get_id())
        cards = customer.get_all_cards()
        if cards is not None:
            for card in cards:
                print("CARD")
                print(card['last_four'])
        else:
            print("cards is None")

    else:
        print("FAIL")


    print("re render")
    return render_template('manage_payment.html', cards=cards)


@bp.route('/make_payment', methods=('GET', 'POST'))
@login_required
def make_payment():
    address = {
        'state': 'State (REQUIRED)',
        'city': 'City (REQUIRED)',
        'street': 'Street (REQUIRED)',
        'zip_code': 'ZIP Code (REQUIRED)'
    }
    print("Creating the card")
    card = CreditCard()
    addr = Address()
    if request.method == 'POST':
        card_type = request.form.get('cardtype')
        cc_number = request.form.get('Payment')
        cvv = request.form.get('CVV')
        expiration_month = request.form.get('month')
        expiration_year = request.form.get('ExpirationYear')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        expiration_date = datetime.datetime.now()
        print(card_type)
        print(int(expiration_month[0:2]))
        if validate_year(expiration_year):
            expiration_date = datetime.datetime(int(expiration_year),
                                                int(expiration_month[0:2]),
                                                1, 1, 1)

        error = None

        customer = Customer()
        if customer.fetch(session['user_id']) and len(customer.get_all_cards()) >= 3:
            error = "Customer has hit limit of 3 cards, cannot add anymore"
        # check that all fields are filled out and valid
        # for BOTH credit card and address
        if cc_number == '' or not validate_cc_number(cc_number):
            error = "Invalid credit card number"
        elif cvv == '' or not validate_cvv(cvv):
            error = "Invalid CVV"
        elif expiration_date == '' or not validate_expiration_date(expiration_date):
            error = "Invalid expiration date"
        elif card_type == '':
            error = "Invalid card type"

        if (error is None and street != '' and city != '' and
            state != '' and zip_code != ''):
            if not validate_zip(zip_code):
                error = 'Zip code must be a valid zip code and '\
                    + 'be entered in ##### or #####-#### format'
            elif not validate_state(state):
                error = 'State must be valid and entered in ## format'

        if error is None:
            addr.create(street=street, city=city,
                        state=state, zip_code=zip_code)

            # get the customer's id via fetching the username
            if customer.fetch(session['user_id']):
                # get the last four
                last_four = cc_number[-4:]
                print("ID:")
                print(customer.get_id())
                card.create(card_number=generate_password_hash(cc_number),
                            customer_id=customer.get_id(),
                            address_id=addr.get_id(),
                            last_four=last_four,
                            cvv=cvv, exp_date=expiration_date,
                            cardtype=card_type)
                customer.send_add_payment_email(card_type)
                # return the home profile
                if request.form.get('checkout'):
                    del session['checkout']
                    return redirect(url_for('CheckoutController.checkout'))
                return redirect(url_for('AccountController.manage_payment'))
            else:
                error = "Invalid customer"

        # else flash the error message
        flash(error)

    return render_template('make_payment.html', address=address)

@bp.route('/edit_payment', methods=('GET','POST'))
@login_required
def edit_payment():
    card_id = request.args.get('cid')
    print(card_id)
    if card_id is not None:
        session['cid'] = card_id
    else:
        card_id = session['cid']

    # fetch card and address
    card = CreditCard()
    card.fetch(card_id)
    addr = Address()
    addr.fetch(card.get_address())

    if request.method == 'POST':
        # on a post, pull the values from each field
        card_num = request.form.get('card_number')
        exp_month = request.form.get('month')
        exp_year = request.form.get('year')
        cvv = request.form.get('cvv')

        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        error = None
        month, year = None, None
        info_changed = False
        month_change, year_change = False, False

        print(exp_month)
        if (exp_month != '' and exp_month is not None and
            exp_month[0:2] != card.get_expiration_date()[5:7]):
            month = exp_month
            month_change = True
        else:
            month = card.get_expiration_date()[5:7]
            print(exp_month)

        print(exp_year)
        if (exp_year != '' and exp_year is not None
            and exp_year != card.get_expiration_date()[0:4]):
            year = exp_year
            year_change = True
            print("year change")
        else:
            year = card.get_expiration_date()[0:4]

        if month is not None and year is not None:
            expiration_date, error = clean_expiration(month, year)
            print("neither is none")
            print(error)
            if error is None and validate_expiration_date(expiration_date):
                card.set_expiration_date(expiration_date)
                print("in this")
                if month_change or year_change:
                    info_changed = True
                print("exp change")
            else:
                error = "Invalid expiration date"
                print("invalid exp date")

        if card_num != '' and validate_cc_number(card_num):
            card.set_cc_number(generate_password_hash(card_num))
            card.set_last_four(card_num[-4:])
            info_changed = True
            print("num change")
        elif card_num != '':
            error = "Invalid card number"
            print(error)

        if cvv != '' and validate_cvv(cvv):
            card.set_cvv(cvv)
            info_changed = True
            print("CVV change")
        elif cvv != '':
            error = "Invalid CVV"

        # set new data for addr
        if street != '':
            addr.set_street(street)
            info_changed = True
            print("Street change")

        if city != '':
            addr.set_city(city)
            info_changed = True
            print("City change")

        if state != '' and validate_state(state):
            addr.set_state(state)
            info_changed = True
            print("State change")
        elif state != '':
            error = 'State must be valid and entered in ## format'

        if zip_code != '' and validate_zip(zip_code):
            addr.set_zip(zip_code)
            info_changed = True
            print("zip change")
        elif zip_code != '':
            error = 'Zip code must be a valid zip code and be entered in ##### or #####-#### format'

        if info_changed:
            # save both and send an email
            card.save()
            addr.save()
            customer = Customer()
            customer.fetch(session['user_id'])
            customer.send_edit_payment_email(card.get_type())

        if error is not None:
            flash(error)


    # use cid to pull up the card and billing address
    # auto fill these in
    credit_card = card.obj_as_dict(card.get_id())
    address = addr.obj_as_dict(card.get_address())
    return render_template('edit_payment.html', address=address, card=credit_card, cid=request.args.get('cid'))

@bp.route('/verify_password', methods=('GET', 'POST'))
@login_required
def verify_password():
    # use previous tools to verify the password
    if request.method == 'POST':
        username = session['user_id']
        password = request.form['password']

        user = get_user(username)

        error = None

        if user is not None:
            error = verify_username_password(username, password,
                                             user.get_password())
        if error is None and user is not None:
            return redirect(
                url_for('ResetPasswordController.reset_password')
            )

        flash(error)

    return render_template('verify_password.html')
