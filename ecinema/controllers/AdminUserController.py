import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ecinema.controllers.LoginController import admin_login_required
from ecinema.tools.validation import (
    validate_name, validate_text, validate_rating,
    validate_category, validate_duration, validate_email,
    validate_address, validate_username, validate_phone
)

from ecinema.models.Customer import Customer
from ecinema.models.CreditCard import CreditCard
from ecinema.models.Address import Address
from ecinema.controllers.RefundController import delete_booking_and_tickets

bp = Blueprint('AdminUsersController', __name__, url_prefix='/')




def safe_delete(customer_id):
    customer = Customer()
    if customer_id and customer.fetch_by_customer_id(customer_id):
        # check that customer has no active bookings
        if not customer.has_active_bookings():
            customer.delete_reviews()
            bookings = customer.get_previous_bookings()
            for booking in bookings:
                delete_booking_and_tickets(booking['booking_id'])

            address = Address()
            # won't delete if it has a card
            address.delete(customer.get_address_id())

            cards = customer.get_all_cards()
            cc = CreditCard()
            for card in cards:
                # delete the card, then the address
                aid = card['aid']
                cc.delete(card['credit_card_id'])
                address.delete(aid)

            customer.delete(customer_id)
            return True
    return False

@bp.route('/manage_users', methods=('GET', 'POST'))
@admin_login_required
def manage_users():
    customer = Customer()

    if request.method == 'POST':
        delete_customer_id = request.form.get('delete_customer_id')
        suspend_customer_id = request.form.get('suspend_customer_id')
        #edit_customer_id = request.form.get('edit_customer_id')

        if delete_customer_id and not safe_delete(delete_customer_id):
            flash("Cannot delete customer, they have active tickets to an upcoming show")
        elif suspend_customer_id and customer.fetch_by_customer_id(suspend_customer_id):
            status = customer.get_status()
            if status == 'active':
                customer.set_status('suspended')
            else:
                customer.set_status('active')
            customer.save()

    # get a list of all users
    customers = customer.get_all_customers()

    return render_template('manage_users.html', customers=customers)

@bp.route('/edit_user/<cid>', methods=('GET', 'POST'))
@admin_login_required
def edit_user(cid):
    customer_id = cid
    customer = Customer()
    print(customer.fetch_by_customer_id(customer_id))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone_number')
        status = request.form.get('state')

        error = None
        change = False

        if first_name and not validate_name(first_name):
            error = "First name is too short or too long"
        elif first_name :
            customer.set_first_name(first_name)
            change = True

        if last_name  and not validate_name(last_name):
            error = "Last name is too short or too long"
        elif last_name :
            customer.set_last_name(last_name)
            change = True

        if phone and not validate_phone(phone):
            error = "Phone number is invalid"
        elif phone:
            customer.set_phone(phone)
            change = True

        if status == 'active' or status == 'inactive' or status == 'suspended':
            customer.set_status(status)
            change = True
        elif status:
            error = "Invalid status"

        if error is not None:
            flash(error)

        if change:
            customer.send_profile_change_email()

        customer.save()


    info = customer.obj_as_dict(customer.get_username())
    customer.save()
    return render_template('edit_user.html', customer=info)

@bp.route('/create_user', methods=('GET', 'POST'))
@admin_login_required
def create_user():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        address_id = request.form['address_id']
        username = request.form['username']

        # validate all data, everything must be correct
        error = None

        if not validate_name(customer_id):
            error = "Customer ID is too short or too long"
        elif not validate_name(first_name):
            error = "First name is too short or too long"
        elif not validate_name(last_name):
            error = "Last name is too short or too long"
        elif not validate_name(email):
            error = "Email is too short or too long"
        elif not validate_name(address_id):
            error = "Address ID is too short or too long"
        elif not validate_name(username):
            error = "Username is too long"
        if error is None:
            # if error is None, create a user
            new_customer = Customer()
            new_customer.create(customer_id=customer_id,first_name=first_name,
                             last_name=last_name, email=email,
                             address_id=address_id, username=username,)

            # then return to add user
            return redirect(url_for('AdminUsersController.manage_users'))

        flash(error)


    return render_template('make_user.html')
