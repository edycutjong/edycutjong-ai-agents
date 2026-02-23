import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Default model
    DEFAULT_MODEL = "gpt-3.5-turbo"
    # App settings
    APP_NAME = "Log to Metrics Converter"
    VERSION = "1.0.0"

    # Default Prometheus scrape interval
    DEFAULT_SCRAPE_INTERVAL = "15s"
