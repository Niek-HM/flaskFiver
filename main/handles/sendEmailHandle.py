import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# HACK Save this in the .env
sender = 'noresponse.informatica@gmail.com'
password = 'asqtmaggxdwmpitn'

def sendPersonal(receiver: str, head: str, body: str, file: str=''): # NOTE Send an email to one singel person
    ##* CREATE THE MESSAGE *##
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = head

    # TODO Add file support

    message.attach(MIMEText(body, "html"))

    text = message.as_string()

    ##* SEND THE MESSAGE *##
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, text)

def sendMass(receivers: list, head: str, body: str, file: str=''):
    ##* CREATE THE MESSAGE *##
    message = MIMEMultipart()
    message['From'] = sender
    message['Bcc'] = ", ".join(receivers)
    message['Subject'] = head

    # TODO Add file support

    message.attach(MIMEText(body, "html"))
    text = message.as_string()

    ##* SEND THE MESSAGE *##
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, text)