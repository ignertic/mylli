import sys
import os
import argparse
from .model import MailingList, sMail
from loguru import logger as log
from platform import uname
import random
from pyfiglet import Figlet
# import sendgrid
#Commands

# add -> add address to mailing list
# broadcast -> broadcast message
# mailist -> return addresses in list
# send -> invoke sending prompt
# stats -> return stats
figFonts = Figlet().getFonts()



parser = argparse.ArgumentParser()

parser.add_argument("--mFrom" , help="Sender Address", default=uname().node+"@mylli.supercode.xo")
parser.add_argument("--to", help="destination address", default="ilovebugsincode@gmail.com" )
parser.add_argument("-s", "--subject", help="Subject of Email", default="I love mylli")
parser.add_argument("-b", "--body", help="Email Body", default="mylli works well")
parser.add_argument("-t", "--template", help="Load Template", default=None)
parser.add_argument("-a", "--add", help="Add Address to Mailing List")
# margs = parser.parse_args()
#Databse Engine to store emails
mylli = MailingList()





def main():
    # Add email to mail cache
    # Prepare email
    args = sys.argv[1:]
    if len(args)==0:
        f=Figlet(random.choice(figFonts))
        print(f.renderText("mylli"))
        print("Simple Mailer by Gishobert (SuperCode) Gwenzi")

    elif args[0] == "add":
        #
        email_addr = args[1]
        mylli.add_addr_to_list([email_addr])
        log.info("Succeessfully Added to MailingList")

        # TODO: regexmto validate email



        #add email addres to mailing list
    elif args[0] == "broadcast":
        #broadcast to addrresses in list
        #subject
        # from
        #body
        # TODO: Parse args properly
        subject, mFrom, body = args[1:]
        mylli.broadcast(subject, mFrom, body)

    elif args[0] == "mailist":
        #return numbered list of mails in list
        print(mylli.get_mailing_list())
    elif args[0] == "send":
        #start email sending prompt
        subject = str(input("Subject: "))
        mFrom = str(input("From: "))
        body = str(input("Body: ")) # TODO: Allo loading from template
        recipients = str(input("Recipients, separate with comma: "))

        for to in recipients.split(","):
            mail_obj = sMail(mFrom,to, subject, body)
            mylli.send_email(mail_obj)
    elif args[0] == "stats":
        #return stats
        pass
    elif args[0] == "blacklist":
        #blacklist addr from list
        pass

    else:
        f=Figlet(random.choice(figFonts))
        print(f.renderText("mylli"))
        print("Bye!!!!")

if __name__ == '__main__':
    main()
