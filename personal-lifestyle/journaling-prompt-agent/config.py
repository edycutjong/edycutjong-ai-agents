import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Data Directory
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# File Paths
JOURNAL_FILE = DATA_DIR / "journal_entries.json"
MOOD_TRACKER_FILE = DATA_DIR / "mood_tracker.json"
EXPORTS_DIR = BASE_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configuration
MODEL_NAME = "gpt-4o"
TEMPERATURE = 0.7
