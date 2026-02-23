import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JULES_API_KEY = os.getenv("JULES_API_KEY")

# Model Configuration
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.2

# Application Settings
APP_NAME = "Technical Blog Reviewer"
APP_DESCRIPTION = "Automated technical blog review agent ensuring accuracy, code correctness, and readability."
