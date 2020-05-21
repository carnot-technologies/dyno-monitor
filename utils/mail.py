import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from threading import Thread


# @TODO: Fetch from environment
EMAIL_HOST = '***REMOVED***'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = '***REMOVED***'
EMAIL_HOST_USER = '***REMOVED***'
SERVER_EMAIL = '***REMOVED***'
RECIPIENTS = ['***REMOVED***']


def send_email(subject, message, recipients=RECIPIENTS):
    msg = MIMEMultipart()
    message = str(message)
    msg['From'] = SERVER_EMAIL
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = str(subject)
    msg.attach(MIMEText(message, 'plain'))

    smtpObj = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    smtpObj.starttls()
    smtpObj.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtpObj.sendmail(msg['From'], recipients, msg.as_string())
    smtpObj.close()


def mail_admins(subject, message, prefix=settings.MAIL_PREFIX):
    if settings.ENABLE_EMAILS:
        modsub = prefix + " " + subject
        t = Thread(target=send_email, args=(modsub, message,))
        t.start()
    return True
