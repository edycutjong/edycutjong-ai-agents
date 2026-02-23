import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # Add other LLM provider keys if needed

    DEFAULT_MONOREPO_TOOL = "turbo"
    DEFAULT_PACKAGE_MANAGER = "pnpm"

    # Model configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))

settings = Config()
