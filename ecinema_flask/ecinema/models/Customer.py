import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, email, text)
        server.quit()
