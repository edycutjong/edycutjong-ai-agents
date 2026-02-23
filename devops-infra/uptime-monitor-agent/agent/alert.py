import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import os

# Add parent directory to sys.path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, WEBHOOK_URL
except ImportError:
    EMAIL_SENDER = None
    EMAIL_PASSWORD = None
    EMAIL_RECIPIENT = None
    EMAIL_SMTP_SERVER = "smtp.gmail.com"
    EMAIL_SMTP_PORT = 587
    WEBHOOK_URL = None

def send_email_alert(subject, body):
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        print("Email config missing. Skipping email alert.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_webhook_alert(message):
    if not WEBHOOK_URL:
        print("Webhook URL missing. Skipping webhook alert.")
        return False

    try:
        payload = {"content": message}
        response = requests.post(WEBHOOK_URL, json=payload)
        return response.status_code == 200 or response.status_code == 204
    except Exception as e:
        print(f"Failed to send webhook: {e}")
        return False

def send_alert(endpoint, error_message, ai_diagnosis=None):
    subject = f"DOWN Alert: {endpoint}"
    body = f"Endpoint: {endpoint} is DOWN.\nError: {error_message}\n\n"

    if ai_diagnosis:
        body += f"AI Diagnosis:\n{ai_diagnosis}\n"

    # Send alerts
    email_sent = send_email_alert(subject, body)
    webhook_sent = send_webhook_alert(body)

    return email_sent, webhook_sent
