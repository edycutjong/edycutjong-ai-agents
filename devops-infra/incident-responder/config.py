import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

# Log Configuration
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "application.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Alert Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
PAGERDUTY_API_KEY = os.getenv("PAGERDUTY_API_KEY")

# Report Configuration
REPORT_OUTPUT_DIR = "reports"
