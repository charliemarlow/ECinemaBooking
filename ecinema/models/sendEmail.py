import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = "ecinemaBookingWebsite@gmail.com"
password = "4050Project"
# email should be a list!!


def sendEmail(email, sub, message):
    receivers = email
    subject = sub

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


#sendEmail(["tmt40253@uga.edu, travis.thurber21@gmail.com"], "Hello Travis", "The Princ of Nigeria needs you're HeLp!")
