import os

import sys
import smtplib
import argparse
from email.mime.text import MIMEText
from email.utils import formatdate
from getpass import getpass

#### Receiver
import poplib
import imaplib
import email
import time

from datetime import datetime,date
import hashlib


# Super class for mail senders
class MailSender:
    def __init__(self, gmail_flag, conf_dct):
        if gmail_flag == 0:
            self.gmail_flag = 0
            self.user = conf_dct['account']
            self.passwd = conf_dct['passwd']
            self.smtp_host = conf_dct['svr_addr']
            self.smtp_port = conf_dct['svr_port']
        elif gmail_flag == 1:
            self.gmail_flag = 1
            self.address = conf_dct['account']
            self.secrets_path = conf_dct['secrets_path']
            self.token_path = conf_dct['token_path']

    def send_mail(self, sender, to, sub, body):
        if self.gmail_flag == 0:
            msg = MIMEText(body)
            msg['Subject'] = sub
            msg['From'] = sender
            msg['To'] = to
            msg['Date'] = formatdate()

            if self.smtp_port == 25:
                smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)

                smtp.ehlo()
                smtp.mail(self.user)
                smtp.rcpt(to)
                smtp.data(msg.as_string())
                smtp.quit()

            elif self.smtp_port == 587 or self.smtp_port == 465:
                smtp = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
                smtp.login(self.user, self.passwd)

                smtp.ehlo()
                smtp.mail(self.user)
                smtp.rcpt(to)
                smtp.data(msg.as_string())
                smtp.quit()
        elif self.gmail_flag == 1:
            GmailApi.GmailApi.precheck(self.address, self.secrets_path, self.token_path)
            api = GmailApi.GmailApi(self.address, self.token_path)
            api.send_message(sender, to, sub, body, 'me')

######################### Receiver
class MailReceiver:
    #def __init__(self, gmail_flag, account, passwd, recv_host, recv_port):
    def __init__(self, gmail_flag, conf_dct):
        if gmail_flag == 0:
            self.gmail_flag = 0
            self.user = conf_dct['account']
            self.passwd = conf_dct['passwd']
            self.recv_host = conf_dct['svr_addr']
            self.recv_port = conf_dct['svr_port']
        elif gmail_flag == 1:
            self.gmail_flag = 1
            self.address = conf_dct['account']
            self.secrets_path = conf_dct['secrets_path']
            self.token_path = conf_dct['token_path']

    def get_body(self, msg):
        body = msg.get_payload(decode=True)
        if type(body) is str:
            char = msg.get_param('charset')
            return str(body, char, 'ignore')
        elif type(body) is bytes:
            return body.decode()

    def get_header(self, msg, name):
        m_header = email.header.decode_header(msg.get(name))
        return str(email.header.make_header(m_header))

    def parse_msg(self, msg) -> dict:
        def _set_dct(keys, values, append_key, append_value):
            keys.append(append_key)
            values.append(append_value)

        keys = list()
        values = list()

        for key in ['Subject', 'To', 'From', 'Date', 'body']:
            if key is 'body':
                _set_dct(keys, values, 'body', self.get_body(msg))
            else:
                _set_dct(keys, values, key, self.get_header(msg, key))

        return dict(zip(keys, values))

    def pop(self, popsv, user, passwd) -> dict:
        # POP Connection
        pop3 = poplib.POP3(popsv)
        pop3.user(user)
        pop3.pass_(passwd)

        # 2021/11/8 commentout by Toshiki Shimatani
        # Loop for each mail
        #for i in range(1, len(pop3.list()[1]) + 1):
        #    # Get a email
        #    msg = '\n'.join(pop3.retr(i)[1])
        #    parse_msg(email.message_from_string(msg))

        # 2021/11/8 added by Toshiki Shimatani
        last = len(pop3.list()[1])
        msg = email.message_from_bytes(b'\r\n'.join(pop3.retr(last)[1]))
        m_dct = self.parse_msg(msg)

        # POP Disconnection
        pop3.quit()

        return m_dct

    def pops(self, popsv, user, passwd) -> dict:
        # POP Connection
        pop3 = poplib.POP3_SSL(popsv, 995)
        pop3.user(user)
        pop3.pass_(passwd)

        # 2020/2/13 commentout by Yuuki OKuda
        # Loop for each mail
        #for i in range(1, len(pop3.list()[1]) + 1):
        #    # Get a email
        #    msg = '\n'.join(pop3.retr(i)[1])
        #    parse_message(email.message_from_string(msg))

        # 2020/2/13 added by Yuuki OKuda
        # Get newest email
        #last = len(pop3.list()[1])
        #msg = '\n'.join(pop3.retr(i)[1])
        #parse_message(email.message_from_string(msg))

        # 2021/11/8 modified by Toshiki Shimatani
        last = len(pop3.list()[1])
        msg = email.message_from_bytes(b'\r\n'.join(pop3.retr(last)[1]))
        m_dct = self.parse_msg(msg)

        # POP Disconnection
        pop3.quit()

        return m_dct

    def imap(imapsv, user, passwd) -> dict:
        # IMAP Connection
        imap = imaplib.IMAP4(imapsv)
        imap.login(user, passwd)

        imap.select()

        typ, data = imap.search(None, '(UNSEEN)')

        # Loop for each mail
        for i in data[0].split():
            # Get a email
            typ, data = imap.fetch(i, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            m_dct = parse_msg(msg)

        # IMAP Disconnection
        imap.close()
        imap.logout()

        return m_dct

    def imaps(imapsv, user, passwd) -> dict:
        # IMAP Connection
        imap = imaplib.IMAP4_SSL(imapsv, 993)
        imap.login(user, passwd)

        imap.select('INBOX')

        typ, data = imap.search(None, '(UNSEEN)')

        # Loop for each mail
        for i in data[0].split():
            # Get a email
            typ, data = imap.fetch(i, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            m_dct = parse_msg(msg)

        # IMAP Disconnection
        imap.close()
        imap.logout()

        return m_dct


    def recv_mail(self, index, sender_addr='sender_addr@sample.com'):
        m_dct = dict()

        if self.gmail_flag == 0:
            if self.recv_port[index] == 110: # pop3
                m_dct = self.pop(self.recv_host[index], self.user[index], self.passwd[index])
            elif self.recv_port[index] == 995 :# pop3s
                m_dct = self.pops(self.recv_host[index], self.user[index], self.passwd[index])
            elif self.recv_port[index] == 143 :# imap
                m_dct = self.imap(self.recv_host[index], self.user[index], self.passwd[index])
            elif self.recv_port[index] == 993 :# imaps
                m_dct = self.imaps(self.recv_host[index], self.user[index], self.passwd[index])
        elif self.gmail_flag == 1:
            GmailApi.GmailApi.precheck(self.address, self.secrets_path, self.token_path)
            api = GmailApi.GmailApi(self.address, self.token_path)
            msg_list = api.recv_messages()
            msg = api.search_msg_by_header(msg_list, 'From', sender_addr) # 送信元アドレスでメッセージを検索
            m_dct = api.parse_msg(msg)

        return m_dct

#########################
def set_smtpconf() -> dict:
    try:
        internal_sender_account = os.environ.get('MAIL_INTERNAL_SENDER_ACCOUNT')
    except Exception as e:
        print("Error: Don't exist <MAIL_INTERNAL_SENDER_ACCOUNT> in setting.sh\n")
        sys.exit(1)

    try:
        internal_sender_account_pass = os.environ.get('MAIL_INTERNAL_SENDER_ACCOUNT_PASS')
    except Exception as e:
        print("Error: Don't exist <MAIL_INTERNAL_SENDER_PASS> in setting.sh\n")
        sys.exit(1)

    try:
        internal_smtpsv_address = os.environ.get('MAIL_INTERNAL_SMTPSV_ADDRESS')
    except Exception as e:
        print("Error: Don't exist <MAIL_INTERNAL_SMTPSV_ADDRESS> in setting.sh\n")
        sys.exit(1)

    try:
        internal_smtpsv_port = int(os.environ.get('MAIL_INTERNAL_SMTPSV_PORT'))
    except Exception as e:
        print("Error: Don't exist <MAIL_INTERNAL_SMTPSV_PORT> in setting.sh\n")
        sys.exit(1)

    d = dict()

    d['account'] = internal_sender_account
    d['passwd'] = internal_sender_account_pass
    d['svr_addr'] = internal_smtpsv_address
    d['svr_port'] = internal_smtpsv_port

    return d

def set_gmailconf() -> dict:
    try:
        gmail_address = os.environ.get('MAIL_GMAIL_ADDRESS')
    except Exception as e:
        print("Error: Don't exist <MAIL_GMAIL_ADDRESS> in setting.sh\n")
        sys.exit(1)

    try:
        gmail_client_secrets_path = os.environ.get('MAIL_GMAIL_CLIENT_SECRETS_PATH')
    except Exception as e:
        print("Error: Don't exist <MAIL_GMAIL_CLIENT_SECRETS_PATH> in setting.sh\n")
        sys.exit(1)

    try:
        gmail_token_path= os.environ.get('MAIL_GMAIL_TOKEN_PATH')
    except Exception as e:
        print("Error: Don't exist <MAIL_GMAIL_TOKEN_PATH> in setting.sh\n")
        sys.exit(1)

    d = dict()

    d['addr'] = gmail_address
    d['secrets_path'] = gmail_client_secrets_path
    d['token_path'] = gmail_token_path

    return d

def set_receiver_conf() -> dict:
    internal_receiver_address = list()
    internal_receiver_account = list()
    internal_receiver_account_pass = list()
    internal_receivesv_address = list()
    internal_receivesv_port = list()

    try:
        num_RecvAccounts = int(os.environ.get('MAIL_INTERNAL_TEST_TARGETS_NUM'))
    except Exception as e:
        print("Error: Don't exist <MAIL_INTERNAL_TEST_TARGETS_NUM> in setting.sh\n")
        sys.exit(1)

    i = 1
    while (i <= num_RecvAccounts):
        try:
            internal_receiver_address.append(os.environ.get('MAIL_INTERNAL_RECEIVER_ADDRESS_' + str(i)))
        except Exception as e:
            print("Error: Don't exist <MAIL_INTERNAL_RECEIVESV_ADDRESS_" + str(i) + "> in setting.sh\n")
            sys.exit(1)

        try:
            internal_receiver_account.append(os.environ.get('MAIL_INTERNAL_RECEIVER_ACCOUNT_' + str(i)))
        except Exception as e:
            print("Error: Don't exist <MAIL_INTERNAL_RECEIVER_ACCOUNT_" + str(i) + "> in setting.sh\n")
            sys.exit(1)

        try:
            internal_receiver_account_pass.append(os.environ.get('MAIL_INTERNAL_RECEIVER_ACCOUNT_PASS_' + str(i)))
        except Exception as e:
            print("Error: Don't exist <MAIL_INTERNAL_RECEIVER_ACCOUNT_PASS_" + str(i) + "> in setting.sh\n")
            sys.exit(1)

        try:
            internal_receivesv_address.append(os.environ.get('MAIL_INTERNAL_RECEIVESV_ADDRESS_' + str(i)))
        except Exception as e:
            print("Error: Don't exist <MAIL_INTERNAL_RECEIVESV_ADDRESS_" + str(i) + "> in setting.sh\n")
            sys.exit(1)

        try:
            internal_receivesv_port.append(int(os.environ.get('MAIL_INTERNAL_RECEIVESV_PORT_' + str(i))))
        except Exception as e:
            print("Error: Don't exist <MAIL_INTERNAL_RECEIVESV_PORT_" + str(i) + "> in setting.sh\n")
            sys.exit(1)

        i += 1

    d = dict()

    d['addr'] = internal_receiver_address
    d['account'] = internal_receiver_account
    d['passwd'] = internal_receiver_account_pass
    d['svr_addr'] = internal_receivesv_address
    d['svr_port'] = internal_receivesv_port

    return d


def main():
    ret = 0
    
    ### Internal Test
    # Internal exsist account => Internal exsist account
    # net-test@swlab.cs.okayama-u.ac.jp => net-test@swlab.cs.okayama-u.ac.jp
    # net-test@swlab.cs.okayama-u.ac.jp => net-mgr@swlab.cs.okayama-u.ac.jp
    sender_conf_dct = set_smtpconf()
    receiver_conf_dct = set_receiver_conf()

    mail_sender = MailSender(0, sender_conf_dct)
    mail_receiver = MailReceiver(0, receiver_conf_dct)

    ts = datetime.now()
    s_ts = ts.strftime('%Y/%m/%d %H:%M:%S')
    hash = hashlib.sha256(s_ts.encode('utf-8')).hexdigest()

    try:
        num_RecvAccounts = int(os.environ.get('MAIL_INTERNAL_TEST_TARGETS_NUM'))
    except Exception as e:
        print("Error: Don't exist <MAIL_INTERNAL_TEST_TARGETS_NUM> in setting.sh\n")
        sys.exit(1)

    i = 0
    while (i < num_RecvAccounts):
        mail_sender.send_mail(sender_conf_dct['account'], receiver_conf_dct['addr'][i], 'Test mail', hash)
        msg_contents_dct = mail_receiver.recv_mail(i)

        if msg_contents_dct['body'] == hash:
            #print("OK")
        else:
            print("Internal Mail Test(Internal => Internal) Failed:")
            ret = 1

        i += 1

    # Internal exsist account => Internal non-exsist account
    # net-test@swlab.cs.okayama-u.ac.jp => noexist@swlab.cs.okayama-u.ac.jp
    non_exist_addr = os.environ.get('MAIL_INTERNAL_RECEIVER_NONEXIST_ACCOUNT')
    try:
        mail_sender.send_mail(sender_conf_dct['account'], non_exist_addr, 'Test mail', hash)
    except Exception as e:
        if e.smtp_code == 554:
            #print("OK")
        else:
            print("NG")
            print("Internal Mail Test(Internal => Internal<non-exist>) Failed:")
            ret = 1

    return ret

if __name__ == "__main__":
    main()


