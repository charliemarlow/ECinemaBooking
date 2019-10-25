from ecinema.tools.sendEmail import sendEmail


class Customer:
    def ___init___(self):
        print("")

    def send_password_reset_email(self, email: str, name: str):
        receivers = [email]
        subject = "Password Change Notification"

        message = """Hey {},

        Your password was just reset at E-Cinema Booking. """\
            + """If you did not authorize this, please reset your """\
            + """password using the forgot my password feature at the login page"""\
            + """

Best,

E-Cinema Booking
        """
        message = message.format(name)
        sendEmail(email, subject, message)

    def sendConfirmationEmail(self, email: str, name: str):
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
