import smtplib
from email.mime.text import MIMEText


def send_email(
    subject: str,
    body: str,
    sender_email: str,
    sender_password: str,
    recipients: list[str],
) -> None:
    if not recipients:
        raise ValueError("Recipient list is empty.")

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipients, msg.as_string())