"""Module to send mails with attachments"""
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

import ssl
import smtplib

from dotenv import dotenv_values

config = dotenv_values(".env")

SENDER_MAIL_ID, SENDER_PASSKEY, RECEIVER_MAIL_ID = config.get(
    'SENDER_MAIL_ID'), config.get('SENDER_PASSKEY'), config.get("RECEIVER_MAIL_ID")


BODY = ""
email_message = EmailMessage()
email_message['From'] = SENDER_MAIL_ID
email_message['To'] = RECEIVER_MAIL_ID
email_message['Subject'] = ""
email_message.set_content(BODY)

email_message.add_alternative(BODY, subtype='html')

with open('<file_path>', 'rb') as attachment_file:
    file_data = attachment_file.read()
    file_name = attachment_file.name.split("/")[-1]

attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(file_data)
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition',
                      f'attachment; filename="{file_name}"')


email_message.attach(attachment)

context = ssl.create_default_context()


SMTP_SERVER, SMTP_PORT = 'smtp.gmail.com', 465
with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
    try:
        smtp.login(SENDER_MAIL_ID, SENDER_PASSKEY)
        smtp.sendmail(SENDER_MAIL_ID,
                      RECEIVER_MAIL_ID, email_message.as_string())
        smtp.close()
    except smtplib.SMTPAuthenticationError as err:
        print(err)
