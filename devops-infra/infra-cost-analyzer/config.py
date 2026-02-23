import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Default currency
    CURRENCY = "USD"
    # Waste thresholds (e.g., low CPU utilization)
    LOW_CPU_THRESHOLD = 5.0  # percentage
    LOW_MEMORY_THRESHOLD = 5.0 # percentage
    # Old snapshot threshold (days)
    OLD_SNAPSHOT_DAYS = 90
