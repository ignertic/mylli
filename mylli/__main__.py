import sys
import os
import argparse
from .model import MailingList, sMail
from loguru import logger as log
from platform import uname
import random
from pyfiglet import Figlet

figFonts = Figlet().getFonts()
mylli = MailingList()


def main():

    args = sys.argv[1:]
    if len(args)==0:
        f=Figlet(random.choice(figFonts))
        print(f.renderText("mylli"))
        print("Simple Mailer by Gishobert (SuperCode) Gwenzi")

    elif args[0] == "add":

        email_addr = args[1]
        mylli.add_addr_to_list([email_addr])
        log.info("Succeessfully Added to MailingList")






    elif args[0] == "broadcast":
        subject, mFrom, body = args[1:]
        mylli.broadcast(subject, mFrom, body)

    elif args[0] == "configure":
        KEY=str(input("Sendgrid Key:>"))
        mylli.set_key(KEY)

    elif args[0] == "mailist":
        print(mylli.get_mailing_list())
    elif args[0] == "send":
        subject = str(input("Subject: "))
        mFrom = str(input("From: "))
        body = str(input("Body: "))
        recipients = str(input("Recipients, separate with comma: "))

        for to in recipients.split(","):
            mail_obj = sMail(mFrom,to, subject, body)
            mylli.send_email(mail_obj)

    else:
        f=Figlet(random.choice(figFonts))
        print(f.renderText("mylli"))
        print("Bye!!!!")

if __name__ == '__main__':
    main()
