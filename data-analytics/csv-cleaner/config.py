import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration for CSV Cleaner."""
    DEFAULT_ENCODING = os.getenv("DEFAULT_ENCODING", "utf-8")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
