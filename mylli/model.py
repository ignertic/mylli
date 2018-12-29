#model
import time
import random
from platform import uname
from loguru import logger as log # TODO: Configure proper logger
import io
import queue

# TODO: Create Stats Model

FROM = uname().node+"@mylli.supercode.xo"
# TODO: Create Custom Queue class
class Mail(object):
    def __init__(self, mFrom, to, subject, body,html_body=None):
        self.mFrom = mFrom
        self.to = to
        self.subject = subject
        self.body = body


class MailingList(object):

    def __init__(self, mails=None, mFrom=FROM):
        super(MailingList, self).__init__()
        self.mails = mails
        self.delay = 5
        self.mail_queue = queue.Queue(100) #maximum Sendgrid limit
        #load date

        #Mail Objects
        # TODO: Load mail objects from COnstrctor

    def add_addr_to_list(self, addrs):
        #Save email address to file for mailing list
        with io.open("mailing_list.xo", "a+") as fh:
            for addr in addrs:
                if addr is "invalid": continue
                fh.write(addr+"\n")
                log.debug("Added {} to Mailing List".format(addr))
                # TODO: Show entry index

    @staticmethod
    def load_addresses(mailing_list="mailing_list.xo"):
        #load addresses from file
        with open(mailing_list, 'r') as fh:
            addrs = fh.read()

            return addrs.split("\n")
    def get_mailing_list(self):
        flist=""
        emails = self.load_addresses()
        for i in emails:
            flist+=str(emails.index(i)) +". " +i+"\n"
        return flist

    def broadcast(self, subject,  body, mFrom=FROM,template=None):
        #broadcast to mailing list
        #load addrs
        recipients = self.load_addresses()
        if len(recipients) > 100:
            log.warning("More than 100 emails detected")
        for rec in recipients:
            if not self.mail_queue.full():
                self.mail_queue.put(Mail(mFrom, rec, subject, body )) # TODO: Allow templates
        self.clear_queue()
        log.info("broadcast Complete")

    def remove_address(self, q=None):
        # TODO: Fix this
        new_addrs =[]
        if q is not None:
            with io.open("mailing_list.xo", "r+") as fh:
                addrs=fh.read()
                fh.truncate() #sorry...
                # print(addrs.split())
                for i in addrs.split():
                    uname = i.split("@")[0]
                    # print(i)
                    # TODO: Can do better here
                    if not uname.startswith(q):
                        new_addrs.append(i)
                fh.close()

        self.add_addr_to_list(new_addrs)


    def send_email(self, mail):
        #sendgrid
        self.mail_queue.put(mail)
        self.clear_queue()
        # self.add_addr_to_list(mail)
        # log.info("enQueued ")


    def clear_queue(self):
        while not self.mail_queue.empty():
            #sendgrid adn send
            _mail = self.mail_queue.get()
            log.info("[+]Email Sent to {} from {}".format(_mail.to, _mail.mFrom))

test = MailingList()
