import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_alert_email(recipient: str, subject: str, body: str) -> tuple[bool, str]:
    smtp_host = os.getenv("ALERT_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("ALERT_SMTP_PORT", "465"))
    smtp_username = os.getenv("ALERT_SMTP_USERNAME")
    smtp_password = os.getenv("ALERT_SMTP_PASSWORD")
    sender = os.getenv("ALERT_FROM_EMAIL", smtp_username or "")

    if not smtp_username or not smtp_password:
        return False, "Email is not configured. Set ALERT_SMTP_USERNAME and ALERT_SMTP_PASSWORD."

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        return False, f"Email delivery failed: {error}"

    return True, "Alert email sent successfully."