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
    validate_phone
)
from ecinema.tools.generate import generate_username

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
            customer.set_username(generate_username(firstname, customer.get_id()))
            customer.save()
            token = generate_confirmation_token(email)
            customer.send_confirmation_email(email, firstname, customer.get_username(), token)
            return redirect(url_for('RegisterController.confirm_registration'))

        flash(error)

    return render_template('registration.html')


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

@bp.route('/register2')
def optional_registration():
    # Pull data from form
    streetAddress = request.form.get('streetaddress')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')

    cardNumber = request.form.get('cardnumber')
    expDate = request.form.get('expdate')
    cvv = request.form.get('cvv')
    cardtype = request.form.get('cardtype')

    error = None

    if not (streetAddress == "" and city == "" and state == "" and zipcode == ""):
        error = 'Please complete your Address Information'
        
    if not (cardNumber == "" and expDate == "" and cvv == "" and cardtype == ""):
        error = 'Please complete your Payment Information'

    if error is None:
        if 'customer' in session:
            address = Address()
            address.create(street=streetAddress, city=city, state=state, zip_code=zipcode)
            session['customer'].set_address_id(address.get_id())
            session['customer'].customer.save()

            creditcard = CreditCard()
            last_four = cardNumber[-4:]
            creditcard.create(cid=session['customer'].customer.get_id(), aid=address.get_id(), cardNumber=cardNumber, 
                            exp_date=expDate, cvv=cvv, type=cardtype, last_four=last_four)
            creditcard.set_customer(session['customer'].customer.get_id())
            creditcard.save()

            token = generate_confirmation_token(session['customer'].get_email())
            session['customer'].customer.send_confirmation_email(session['customer'].get_email, session['customer'].get_firstname, token)

            return redirect(url_for('RegisterController.confirm_registration'))
        else:
            print("Something wrong with option2")
        
    
                  
    return render_template('registration_optional.html')
