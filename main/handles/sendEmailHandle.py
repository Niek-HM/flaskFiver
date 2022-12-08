import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendPersonal(receiver: str, head: str, body: str, file: str): #! Make sure it works since google disabled email macros some time ago...
    sender = 'noresponse.informatica@gmail.com'
    password = 'Informatica1!'

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = head

    message.attach(MIMEText(body, "plain"))

    # Maybe add file support?

    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, text)

def sendMass(receivers: list, head: str, body: str, file: str):
    sender = 'noresponse.informatica@gmail.com'
    password = 'yvdsktarqhgusntd'

    message = MIMEMultipart()
    message['From'] = sender
    message['Bcc'] = ", ".join(receivers)
    message['Subject'] = head

    message.attach(MIMEText(body, "html"))

    # Maybe add file support

    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, text)