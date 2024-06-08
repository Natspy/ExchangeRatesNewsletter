import smtplib
from datetime import datetime
from trash.config import *
from email.mime.text import MIMEText

subject = "Exchange rates - Newsletter"
current_date = datetime.now().strftime("%d.%m.%Y")
body = f"Current exchange rates for day {current_date}"
recipients = [SENDER, "nataliakarczewskapp@gmail.com"]


def send_email(subject, body, sender, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, APP_PASSWORD)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent")


send_email(subject, body, SENDER, recipients)
