import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Default model
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    # Mock mode for testing/demo without API key
    MOCK_MODE = os.getenv("MOCK_MODE", "True").lower() == "true"
