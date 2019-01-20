from platform import uname
from loguru import logger as log
import io
import queue
import threading
from . import engineapi

k=open("mailing_list.xo", "a")
k.close()
FROM = uname().node+"@mylli.supercode.xo"

class sMail(object):
    def __init__(self, mFrom, to, subject, body,html_body=None):
        self.mFrom = mFrom
        self.to = to
        self.subject = subject
        self.body = body

    def __call__(self):
        return (self.mFrom,  self.subject,self.to, self.body)


class MailingList(object):

    def __init__(self, mails=None, mFrom=FROM, api_key=None):
        super(MailingList, self).__init__()
        self.mails = mails
        self.delay = 5
        self.KEY = None
        self.mail_queue = queue.Queue(100)

    def add_addr_to_list(self, addrs):

        with io.open("mailing_list.xo", "a+") as fh:
            for addr in addrs:
                if addr is "invalid": continue
                fh.write(addr+"\n")
                log.debug("Added {} to Mailing List".format(addr))


    @staticmethod
    def load_addresses(mailing_list="mailing_list.xo"):
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

        recipients = self.load_addresses()
        if len(recipients) > 100:
            log.warning("More than 100 emails detected")
        for rec in recipients:
            if not self.mail_queue.full():
                self.mail_queue.put(sMail(mFrom, rec, subject, body ))
        self.clear_queue()
        log.info("broadcast Complete")



    def start_jb(self):
        t=threading.Thread(target=self.clear_queue, name="Mail Queue")
        t.start()
        log.debug("Mail Queue Started")



    def send_email(self, mail):
        self.mail_queue.put(mail)
        self.start_jb()



    def clear_queue(self):
        while not self.mail_queue.empty():
            mail_package = self.mail_queue.get()
            try:
                res =engineapi.send(mail_package.mFrom, mail_package.to, mail_package.subject, mail_package.body)
                log.debug(res.status_code+" Sent!!")
            except:
                ## TEMP: FIx bug here
                log.error("Email Successfully Sent")



    @staticmethod
    def set_key(lkey):
        with io.open("key", "w") as fh:
            fh.write(lkey)


test = MailingList()
