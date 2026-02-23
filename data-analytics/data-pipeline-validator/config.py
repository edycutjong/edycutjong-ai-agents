import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = "gpt-4o"
    VALIDATION_REPORT_DIR = "reports"

    # Supported File Types
    SUPPORTED_EXTENSIONS = [".csv", ".parquet", ".xlsx"]

config = Config()
