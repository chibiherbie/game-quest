import os
import smtplib
import mimetypes
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template


def send_email(email, name, date, address, url):
    addr_from = os.getenv('FROM')
    password = os.getenv('PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = email
    msg['Subject'] = 'Регестрация на игру'
    msg.attach(MIMEText(render_template('email_msg.html', name=name, date=date, address=address, url=url),
                        'html'))

    server = smtplib.SMTP_SSL(os.getenv('HOST_E'), os.getenv('PORT_E'))
    server.login(addr_from, password)

    server.send_message(msg)
    server.quit()
    print('СООБЩЕНИЕ ОТПРАВЛЕНО')