import smtplib
from datetime import datetime
from config import SENDER, APP_PASSWORD
from email.mime.text import MIMEText

def send_email(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(SENDER, APP_PASSWORD)
        smtp_server.sendmail(SENDER, recipients, msg.as_string())
    print("Message sent")
