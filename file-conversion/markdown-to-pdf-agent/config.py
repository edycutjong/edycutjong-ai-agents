import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Application Defaults
DEFAULT_THEME = "default"
DEFAULT_INPUT_DIR = os.path.join(os.path.dirname(__file__), "input")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
DEFAULT_MODEL = "gpt-4o"

# Ensure directories exist
os.makedirs(DEFAULT_INPUT_DIR, exist_ok=True)
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
