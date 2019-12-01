from ecinema.controllers.CheckoutController import clear_booking_info
from ecinema.controllers.SeatSelectionController import clear_ticket_ids, reset_available_seats

from flask import session

# temporary stop gap
# need to have a job that clears tickets quicker


def clear_all_booking():
    if not session.get('ticket_ids'):
        return
    reset_available_seats()
    clear_ticket_ids()
    clear_booking_info()
