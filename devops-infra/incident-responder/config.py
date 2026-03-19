import os  # pragma: no cover
from dotenv import load_dotenv  # pragma: no cover

load_dotenv()  # pragma: no cover

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # pragma: no cover
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")  # pragma: no cover

# Log Configuration
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "application.log")  # pragma: no cover
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # pragma: no cover

# Alert Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # pragma: no cover
PAGERDUTY_API_KEY = os.getenv("PAGERDUTY_API_KEY")  # pragma: no cover

# Report Configuration
REPORT_OUTPUT_DIR = "reports"  # pragma: no cover
