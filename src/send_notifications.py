import os
import smtplib
from email.message import EmailMessage

def send_email(pdf_path):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    msg = EmailMessage()
    msg["Subject"] = "Weekly Luxury Hotel Deals 🏨"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Here’s your weekly summary of discounted luxury hotels!")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
