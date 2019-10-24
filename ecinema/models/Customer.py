from ecinema.tools.sendEmail import send_email


class Customer:
    def ___init___(self):
        print("")

    def send_confirmation_email(self, email: str, name: str):
        sender = "ecinemaBookingWebsite@gmail.com"
        password = "4050Project"
        receivers = [email]
        subject = "Registration Confirmation"

        message = """Hey {},

        You have successfully registered an account at E-Cinema """\
            + """Booking under this email address. We're looking """\
            + """forward to seeing you soon!"""\
            + """

Best,

E-Cinema Booking
        """
        message = message.format(name)

        send_email(email, subject, message)
