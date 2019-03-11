import smtplib
import sys
import os
from email.mime.text import MIMEText
sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'))
from config import Config

class EmailHelper():
    def __init__(self):
        self.config = Config()
        self.email_obj = self.config.get('email')

    def send_mail(self, message):
        msg = MIMEText(message['body'])
        msg['Subject'] = message['subject']
        msg['From'] = self.email_obj['notification_email']
        msg['To'] = message['to']

        # Send the message via our own SMTP server.
        s = smtplib.SMTP(
            self.email_obj['smtp_server'], port=self.email_obj['smtp_port'])
        s.send_message(msg)
        s.quit()
