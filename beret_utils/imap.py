#!/usr/bin/env python
# -*- coding: utf-8 -*-
import email
from email.header import decode_header
from email.parser import Parser as EmailParser
from email.utils import parseaddr
from imaplib import IMAP4
from io import StringIO


class NotSupportedMailFormat(Exception):
    pass


def parse_attachment(message_part):
    """
    parse attachement file
    """
    content_disposition = message_part.get("Content-Disposition", None)
    if content_disposition:
        dispositions = content_disposition.strip().split(";")
        if bool(content_disposition and dispositions[0].lower() == "attachment"):

            file_data = message_part.get_payload(decode=True)
            attachment = StringIO(file_data)
            attachment.data = file_data
            attachment.content_type = message_part.get_content_type()
            attachment.size = len(file_data)
            attachment.name = None
            attachment.create_date = None
            attachment.mod_date = None
            attachment.read_date = None

            for param in dispositions[1:]:
                name, value = param.split("=")
                if value[0] == '"':
                    value = value[1:]
                if value[-1] == '"':
                    value = value[:-1]
                if value[0] == "'":
                    value = value[1:]
                if value[-1] == "'":
                    value = value[:-1]
                name = name.lower()
                if "filename" in name:
                    attachment.name = value
                elif "create-date" in name:
                    attachment.create_date = value
                elif "modification-date" in name:
                    attachment.mod_date = value
                elif "read-date" in name:
                    attachment.read_date = value
            return attachment

    return None


def parse_email_content(content):
    """
    parse email content
    """
    p = EmailParser()
    msgobj = p.parse(StringIO(content), False)
    if msgobj['Subject'] is not None:
        decodefrag = decode_header(msgobj['Subject'])
        subj_fragments = []
        for s, enc in decodefrag:
            if enc:
                s = s.encode('utf8', 'replace')
            subj_fragments.append(s)
        subject = ''.join(subj_fragments)
    else:
        subject = None

    attachments = []
    text = None
    body = None
    html = None
    for part in msgobj.walk():
        charset = part.get_content_charset()
        if not charset:
            charset = 'utf-8'
        attachment = parse_attachment(part)
        if attachment:
            attachments.append(attachment)
        elif part.get_content_type() == "text/plain":
            if body is None:
                body = ""
            if text is None:
                text = ""
            text += str(
                part.get_payload(decode=True),
                charset,
                'replace'
            )
            body += str(
                part.get_payload(decode=True),
                charset,
                'replace'
            ).encode('utf8', 'replace')
        elif part.get_content_type() == "text/html":
            if html is None:
                html = ""
            html += str(
                part.get_payload(decode=True),
                charset,
                'replace'
            ).encode('utf8', 'replace')
    return {
        'subject':     subject,
        'body':        body,
        'html':        html,
        'from':        parseaddr(msgobj.get('From'))[1],
        'to':          parseaddr(msgobj.get('To'))[1],
        'cc':          parseaddr(msgobj.get('Cc'))[1],
        'reply_to':    parseaddr(msgobj.get('Reply-To'))[1],
        'attachments': attachments,
    }


class Imap():
    """
    Parse mails from imap server..
    """

    help = "Parse mails from settings.IMAP_SERVER"

    def __init__(self, *args, **kwargs):
        self.imap_server = kwargs.get('imap_server', None)
        self.imap_login = kwargs.get('imap_login', None)
        self.imap_passwd = kwargs.get('imap_passwd', None)
        self.parse_mail = kwargs.get('parse', self._get_parse)
        self.feedback = False

    def open(self):
        self.mailbox = IMAP4(self.imap_server)
        self.mailbox.login(self.imap_login, self.imap_passwd)
        self.mailbox.select()

    def _get_parse(self):
        def _parse(mail=None, *args, **kwargs):
            return mail

        return _parse

    def get_list(self):
        '''
        get list of message's numbers in main mailbox
        '''
        typ, data = self.mailbox.search(None, 'UNSEEN')
        nr_list = data[0].split(' ')
        if len(nr_list) == 1 and nr_list[0] == '':
            return []
        else:
            return nr_list

    def iterator(self):
        for number in self.get_list():
            typ, data = self.mailbox.fetch(number, '(RFC822 UID BODY[TEXT])')
            if data and len(data) > 1:
                mail = parse_email_content(email.message_from_string(data[0][1]))
                yield mail
            self.set_seen(number)
        rest = self.get_list()
        if len(rest) > 0:
            yield from self.iterator()

    def parse(self, _parse=None):
        '''
        parse all mails from imap mailbox
        '''
        return map(self.parse_mail, self.iterator())

    def set_seen(self, number):
        '''
        Set mail as seen
        '''
        self.mailbox.store(number, '+FLAGS', '\\Seen')
        self.mailbox.expunge()

    def mv_mail(self, number, mbox_name):
        '''
        move message to internal mailbox
        @param number: message number in main mailbox
        @param mbox_name: internal mailbox name
        '''
        self.mailbox.copy(number, "INBOX.%s" % mbox_name)
        self.mailbox.store(number, '+FLAGS', '\\Deleted')
        self.mailbox.expunge()

    def close(self):
        if self.mailbox:
            self.mailbox.close()
            self.mailbox.logout()

    def __del__(self, *args, **kwargs):
        self.close()
