#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header

class EmailBuilder:
  def __init__(self, subject: str, content: str, from_alias='', to_alias=''):
    self._subject = subject
    self._content = content
    self._from_alias = from_alias
    self._to_alias = to_alias

  def to_email(self, send_addr: str, recv_addr = '') -> str:
    email = MIMEText(self._content, 'html', 'utf-8')
    email['From'] = Header(self._from_alias and self._from_alias or send_addr, 'utf-8')
    email['From'].append('<'+send_addr+'>', charset='ascii')
    email['To'] = Header(self._to_alias and self._to_alias or recv_addr, 'utf-8')
    if recv_addr:
      email['To'].append('<'+recv_addr+'>', charset='ascii')
    email['Subject'] = Header(self._subject, 'utf-8')
    return email.as_string()

  def to_email_batch(self, send_addr: str, recv_addrs: 'list[str]'):
    email = MIMEText(self._content, 'html', 'utf-8')
    email['From'] = Header(self._from_alias and self._from_alias or send_addr, 'utf-8')
    email['From'].append('<'+send_addr+'>', charset='ascii')
    #email['To'] = Header(self._to_alias and self._to_alias or '', 'utf-8')
    email['To'] = Header()

    for recv_addr in recv_addrs:
      email['To'].append(recv_addr, charset='utf-8')
      email['To'].append('<'+recv_addr+'>', charset='ascii')
    email['Subject'] = Header(self._subject, 'utf-8')
    return email.as_string()

class EmailSender:
  def __init__(self, send_addr, passwd, domain='', ssl_port=465):
    self._send_addr = send_addr.strip()
    self._passwd = passwd
    domain = domain.strip()
    if not domain:
      fragments = self._send_addr.split('@')
      if len(fragments) < 2:
        raise Exception('SMTP domain not given, and given email address has no @ to split.')
      self._domain = fragments[-1]
    else:
      self._domain = domain
    self._ssl_port = ssl_port
    self._smtpObj = None

  # We don't handle smtplib.SMTPException
  def send(self, eb: EmailBuilder, recv_addrs: 'list[str]'):
    if len(recv_addrs) == 0: return False

    if not self._smtpObj:
      self._smtpObj = smtplib.SMTP_SSL(self._domain, self._ssl_port)
      self._smtpObj.login(self._send_addr, self._passwd)

    if eb._to_alias:
      self._smtpObj.sendmail(self._send_addr, recv_addrs, eb.to_email_batch(self._send_addr, recv_addrs))
    else:
      for recv_addr in recv_addrs:
        self._smtpObj.sendmail(self._send_addr, [recv_addr], eb.to_email(self._send_addr, recv_addr))

    return True

TEST_SENDER = ''
TEST_PASSWD = ''
TEST_RECVERS = []

if __name__ == '__main__':
  #eb = EmailBuilder('Test', 'This is the test body.', 'TrickSender', 'TrickReceiver')
  #print(eb.to_email(TEST_SENDER, TEST_RECVERS[0]))
  #print(eb.to_email_batch(TEST_SENDER, TEST_RECVERS))

  es = EmailSender(TEST_SENDER, TEST_PASSWD)
  es.send(EmailBuilder('Test', 'This is the test body.', 'TrickSender', 'TrickReceiver'), TEST_RECVERS)
