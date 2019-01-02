#model
import time
import random
from platform import uname
from loguru import logger as log # TODO: Configure proper logger
import io
import queue
import sendgrid
import threading


from . import engineapi
# TODO: Create Stats Model
k=open("mailing_list.xo", "a")
k.close()
FROM = uname().node+"@mylli.supercode.xo"
# TODO: Create Custom Queue class
class sMail(object):
    def __init__(self, mFrom, to, subject, body,html_body=None):
        self.mFrom = mFrom
        self.to = to
        self.subject = subject
        self.body = body

    def __call__(self):
        #return tuple
        return (self.mFrom,  self.subject,self.to, self.body)


class MailingList(object):

    def __init__(self, mails=None, mFrom=FROM, api_key=None):
        super(MailingList, self).__init__()
        self.mails = mails
        self.delay = 5
        self.KEY = None

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
                self.mail_queue.put(sMail(mFrom, rec, subject, body )) # TODO: Allow templates
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


    def start_jb(self):
        t=threading.Thread(target=self.clear_queue, name="Mail Queue")
        t.start()
        log.debug("Mail Queue Started")



    def send_email(self, mail):
        #sendgrid
        # TODO: Refactor the whole class and inherit from sendgrid
        self.mail_queue.put(mail)
        self.start_jb()
        # self.add_addr_to_list(mail)
        # log.info("enQueued ")


    def clear_queue(self):

        while not self.mail_queue.empty():
            #sendgrid adn send
            # TODO: Error Handling
            mail_package = self.mail_queue.get()
            res =engineapi.send(mail_package.mFrom, mail_package.to, mail_package.subject, mail_package.body)
            log.debug(res.status_code)

    @staticmethod
    def set_key(lkey):
        with io.open("key", "w") as fh:
            fh.write(lkey)


test = MailingList()
