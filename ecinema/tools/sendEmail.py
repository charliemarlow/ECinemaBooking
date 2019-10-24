import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

sender = "ecinemaBookingWebsite@gmail.com"
password = "4050Project"


def send_email(email: List[str], sub: str, message: str):
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
