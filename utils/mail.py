import logging
import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread


def send_email_raw(subject, message, recipients=settings.RECIPIENTS):
    """
    :subject: string,
    :message: string,
    :recipient: list of string email addresses
    """
    if settings.EMAIL_HOST and settings.EMAIL_PORT and settings.EMAIL_HOST_USER \
            and settings.EMAIL_HOST_PASSWORD and settings.SERVER_EMAIL and recipients:
        msg = MIMEMultipart()
        message = str(message)
        msg['From'] = settings.SERVER_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = str(subject)
        msg.attach(MIMEText(message, 'plain'))

        smtpObj = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtpObj.starttls()
        smtpObj.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtpObj.sendmail(msg['From'], recipients, msg.as_string())
        smtpObj.close()

    else:
        logging.error("Please ensure EMAIL configs and RECIPIENTS are correct")


def send_email(subject, message, prefix=settings.EMAIL_PREFIX):
    if settings.ENABLE_EMAILS:
        modsub = prefix + " " + subject
        t = Thread(target=send_email_raw, args=(modsub, message,))
        t.start()


def mail_admins(subject, body):
    if settings.ENABLE_EMAILS:
        from django.core.mail import mail_admins as django_mail_admins
        modsub = settings.EMAIL_PREFIX + " " + subject
        t = Thread(target=django_mail_admins, args=(modsub, body,))
        t.start()
