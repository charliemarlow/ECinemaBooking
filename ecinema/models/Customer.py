import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .sendEmail import sendEmail


class Customer:
    def ___init___(self):
        print("initting")

    def sendConfirmationEmail(self, email, name):
        sender = "ecinemaBookingWebsite@gmail.com"
        password = "4050Project"
        receivers = [email]
        subject = "Registration Confirmation"

        message = """Hey {},

        You have successfully registered an account at E-Cinema Booking under this email address. We're looking forward to seeing you soon!

        Best,

        E-Cinema Booking
        """.format(name)

        sendEmail(email, subject, message)
