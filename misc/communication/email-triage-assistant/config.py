import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App Settings
    APP_NAME = "Email Triage Assistant"
    VERSION = "1.0.0"

    # LLM Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Email Settings
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # Default Categories
    CATEGORIES = ["Urgent", "Work", "Personal", "Newsletter", "Spam", "Other"]
