import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration for LLM Cost Calculator."""
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), "usage_data.json")
