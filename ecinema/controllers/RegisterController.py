import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ecinema.models.Customer import Customer
from ecinema.models.Address import Address
from ecinema.models.CreditCard import CreditCard

from ecinema.tools.token import (
    generate_confirmation_token, confirm_token
)
from ecinema.tools.validation import (
    validate_name, validate_password, validate_email,
    validate_username, validate_unique_email,
    validate_phone, validate_address, validate_card
)
from ecinema.tools.generate import generate_username
from ecinema.tools.clean import clean_expiration

from ecinema.controllers.LoginController import logout_required, setup_session

bp = Blueprint('RegisterController', __name__, url_prefix='/')


@bp.route('/register', methods=('GET', 'POST'))
@logout_required
def register():

    # if the submit button has been presselsd...
    if request.method == 'POST':
        # pull data from forms
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        confirmation = request.form['confirm']
        phonenumber = request.form['phone']
        email = request.form['email']
        username = email

        # IMPORTANT: non-required fields should use the .get method
        subscribe = str(request.form.get('subscribe') is not None)

        error = None

        # validate the fields
        # per issue 7, we'll change this to javascript
        if not validate_name(firstname):
            print(firstname)
            error = "First name is required"
        elif not validate_name(lastname):
            error = "Last name is required"
        elif not validate_password(password, confirmation):
            error = 'Password is required and must be at least 8 '\
                + 'characters with 1 uppercase, and 1 number'
        elif not username:
            error = 'Username is required'
        elif not validate_email(email):
            error = 'Email is required and must be valid'
        elif not validate_unique_email(email):
            error = 'Email is already registered to an account'
        elif not validate_phone(phonenumber):
            error = 'Phone number is invalid'

        # create a new user
        if error is None:
            customer = Customer()
            customer.create(first_name=firstname, last_name=lastname,
                            password=generate_password_hash(password),
                            username=username, email=email,
                            subscribe_to_promo=subscribe,
                            phone=phonenumber)
            customer.set_status('inactive')
            customer.set_username(
                generate_username(
                    firstname,
                    customer.get_id()))
            customer.save()

            token = generate_confirmation_token(email)
            customer.send_confirmation_email(
                email, firstname, customer.get_username(), token)
            session['customer_id'] = customer.get_id()
            session['customer_username'] = customer.get_username()
            return redirect(url_for('RegisterController.optional_register'))

        flash(error)

    return render_template('registration.html')


@bp.route('/optional_register', methods=('GET', 'POST'))
def optional_register():
    if request.method == 'POST':
        # 1. get all input
        home_street = request.form.get('hstreet')
        home_city = request.form.get('hcity')
        home_state = request.form.get('hstate')
        home_zip = request.form.get('hzip')
        filled_home = (home_street != '' and home_city != ''
                       and home_state != '' and home_zip != '')
        print(filled_home)

        card_type = request.form.get('cardtype')
        card_number = request.form.get('card_number')
        expiration_month = request.form.get('exp_month')
        expiration_year = request.form.get('exp_year')
        cvv = request.form.get('cvv')
        filled_card = (card_type != '' and card_number != ''
                       and expiration_month != '' and
                       expiration_year != '' and cvv != '')
        print(filled_card)

        billing_same_as_home = request.form.get('billing') is not None
        billing_street = request.form.get('bstreet')
        billing_city = request.form.get('bcity')
        billing_state = request.form.get('bstate')
        billing_zip = request.form.get('bzip')
        filled_billing = (billing_street != '' and billing_state != ''
                          and billing_city != '' and billing_zip != '')
        print(filled_billing)

        error = None
        if filled_home:
            # validate home address
            error = validate_address(home_street, home_city,
                                     home_state, home_zip)

        error = None
        if filled_card:
            # validate credit card
            expiration_date = None
            if expiration_month is not None and expiration_year is not None:
                expiration_date, error = clean_expiration(expiration_month,
                                                          expiration_year)
                print(error)
            else:
                error = "Expiration date month and year were filled out incorrectly"
                print(error)

            if error is None:
                error = validate_card(card_type, card_number,
                                      expiration_date, cvv)
                print(error)

            # if billing checkbox is None, then validate billing
            if not billing_same_as_home and filled_billing:
                error = validate_address(billing_street, billing_city,
                                         billing_state, billing_zip)
                print(error)
            elif not billing_same_as_home and not filled_billing:
                error = "Billing address should be filled out"

            if billing_same_as_home and not filled_home:
                error = "Billing address required when home address is not filled out"
                print(error)

        # then
        # create the home address
        home_addr = None
        if filled_home and error is None:
            home_addr = Address()
            home_addr.create(street=home_street, city=home_city,
                             state=home_state, zip_code=home_zip)
            # fetch the customer, set their address
            customer = Customer()
            if customer.fetch(session['customer_username']):
                customer.set_address_id(home_addr.get_id())
                customer.save()
                print("Successfully saved addr to customer")
            else:
                print("error fetching customer")
                error = "Error fetching customer"

        if filled_card and error is None:
            # if sameBillingAshome then set credit cards aid to addr
            card_addr_id = None
            if billing_same_as_home:
                if home_addr is not None:
                    card_addr_id = home_addr.get_id()
            else:
                # else, create a new address and set credit cards aid to
                # billAddr
                bill_addr = Address()
                bill_addr.create(street=billing_street, city=billing_city,
                                 state=billing_state, zip_code=billing_zip)
                card_addr_id = bill_addr.get_id()

            # then create the credit card
            card = CreditCard()
            last_four = card_number[-4:]
            card.create(card_number=generate_password_hash(card_number),
                        customer_id=session['customer_id'],
                        address_id=card_addr_id,
                        last_four=last_four,
                        cvv=cvv,
                        exp_date=expiration_date,
                        cardtype=card_type)

        if error is None:
            # delete the session variable
            del session['customer_id']
            del session['customer_username']

            # redirect to confirmaiton
            return redirect(url_for('RegisterController.confirm_registration'))

        flash(error)

    return render_template('optional_register.html')


@bp.route('/confirm_account/<token>')
def confirm_account(token):
    print("account is being confirmed")
    try:
        email = confirm_token(token, expiration=86400)
    except BaseException:
        flash("The confirmation link is invalid or has expired")
        # return a failure page here
        return redirect(
            url_for('RegisterController.account_verification_fail'))

    customer = Customer()

    if customer.fetch_by_email(email):
        setup_session(customer.get_username(), False)
        if customer.get_status() == 'inactive':
            customer.set_status('active')
            customer.save()
            return redirect(
                url_for('RegisterController.account_verification_success'))
        else:
            return redirect(url_for('IndexController.index'))

    # some failure page
    return redirect(url_for('RegisterController.account_verification_fail'))


@bp.route('/account_verification_success')
def account_verification_success():
    return render_template('verify_account_success.html')


@bp.route('/account_verification_fail')
def account_verification_fail():
    return render_template('verify_account_fail.html')


@bp.route('verify_account.html')
def verify_account():
    return render_template('verify_account.html')


@bp.route('/confirm_registration')
@logout_required
def confirm_registration():
    return render_template('register_confirm.html')
