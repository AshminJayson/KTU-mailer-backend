"""Module to send mails with attachments"""
import ssl
import smtplib
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from dotenv import dotenv_values
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

config = dotenv_values(SCRIPT_DIR + '\.env')
from .store import get_subscribers  # nopep8


SENDER_MAIL_ID, SENDER_PASSKEY, RECEIVER_MAIL_ID = config.get(
    'SENDER_MAIL_ID'), config.get('SENDER_PASSKEY'), config.get("RECEIVER_MAIL_ID")


def send_through_smtp(email_message: EmailMessage, recipient_email_id: str):

    context = ssl.create_default_context()
    SMTP_SERVER, SMTP_PORT = 'smtp.gmail.com', 465
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as smtp:
        try:
            smtp.login(SENDER_MAIL_ID, SENDER_PASSKEY)
            smtp.sendmail(SENDER_MAIL_ID,
                          recipient_email_id, email_message.as_string())
            smtp.close()
        except smtplib.SMTPAuthenticationError as err:
            print(err)


def get_email_basic_body(body, subject):
    email_message = EmailMessage()
    email_message['From'] = SENDER_MAIL_ID
    email_message['To'] = RECEIVER_MAIL_ID
    email_message['Subject'] = subject
    email_message.set_content(body)

    return email_message


def get_attachment(file_data, file_name):
    # If reading from file
    # with open('<file_path>', 'rb') as attachment_file:
    #     file_data = attachment_file.read()
    #     file_name = attachment_file.name.split("/")[-1]

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(file_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition',
                          f'attachment; filename="{file_name}"')

    return attachment


def send_mail_to_all_users(body, subject, file_data, file_name):
    for recipient_email_id, recipient_uuid in get_subscribers():
        email_message = get_email_basic_body(
            body=body, subject=subject)
        if file_data:
            email_message.add_alternative(body, subtype='html')
            email_message.attach(get_attachment(
                file_data=file_data, file_name=file_name))

        send_through_smtp(email_message=email_message,
                          recipient_email_id=recipient_email_id)
