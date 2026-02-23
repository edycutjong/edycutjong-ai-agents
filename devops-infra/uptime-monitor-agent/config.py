import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONITOR_ENDPOINTS = os.getenv("MONITOR_ENDPOINTS", "").split(",")
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", 60))

# Email Config
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))

# Webhook Config
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Database Config
DATABASE_URL = "sqlite:///uptime.db"
