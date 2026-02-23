import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TIMEZONE = "UTC"  # Default timezone for scheduling
DEFAULT_MEETING_DURATION = 60  # minutes

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables. Set it in .env file.")
