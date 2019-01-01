import sendgrid
from sendgrid.helpers.mail import *
import random
key = ['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','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']


def send(from_email, to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(apikey=random.choice(key))
    from_email = Email(from_email)
    to_email = Email(to_email)
    content = Content('text/plain', body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print('sent email')
    print(response.status_code)
    return response
