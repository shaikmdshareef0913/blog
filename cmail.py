import smtplib
from smtplib import SMTP
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('shareefshareef0913@gmail.com','iukr mbtn trmx kuhd')
    msg=EmailMessage()
    msg['From']='shareefshareef0913@gmail.com'
    msg['subject']=subject
    msg['To']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()