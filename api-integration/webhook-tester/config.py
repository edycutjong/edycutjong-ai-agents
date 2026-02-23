import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration for Webhook Tester."""
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8765"))
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), "webhooks.json")
