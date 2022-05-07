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
    email['To'] = Header(self._to_alias and self._to_alias or recv_addr, 'utf-8')
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

  # We don't handle smtplib.SMTPException
  def send(self, eb: EmailBuilder, recv_addrs: 'list[str]'):
    if len(recv_addrs) == 0: return False

    smtpObj = smtplib.SMTP_SSL(self._domain, self._ssl_port)
    smtpObj.login(self._send_addr, self._passwd)
    if eb._to_alias:
      smtpObj.sendmail(self._send_addr, recv_addrs, eb.to_email(self._send_addr, ''))
    else:
      for recv_addr in recv_addrs:
        smtpObj.sendmail(self._send_addr, [recv_addr], eb.to_email(self._send_addr, recv_addr))

TEST_SENDER = ''
TEST_PASSWD = ''
TEST_RECVERS = ['']

if __name__ == '__main__':
  es = EmailSender(TEST_SENDER, TEST_PASSWD)
  es.send(EmailBuilder('Test', 'This is the test body.', 'TrickSender', 'TrickReceiver'), TEST_RECVERS)
