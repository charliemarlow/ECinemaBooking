from ecinema.tools.sendEmail import sendEmail


class Customer:
    def ___init___(self):
        print("")

    def sendConfirmationEmail(self, email, name):
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

        sendEmail(email, subject, message)
