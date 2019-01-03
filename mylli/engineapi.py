import sendgrid
from sendgrid.helpers.mail import *
import random

try:
    with open("key", 'r') as fh:
        keys=fh.read()
except FileNotFoundError as e:
    with open("key", "w") as fh:
        KEY=str(input("Paste SendGrid API Key:  "))
        fh.write(KEY)
        keys=KEY


def send(from_email, to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(apikey=keys)
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content('text/plain', body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response
