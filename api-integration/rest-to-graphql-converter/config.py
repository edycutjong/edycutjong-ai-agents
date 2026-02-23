import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4-turbo"  # Or gpt-3.5-turbo if cost is a concern, but we want premium quality.
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

config = Config()
