"""Configuration for Habit Coach agent."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Agent configuration."""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL = os.getenv("MODEL", "gpt-4o-mini")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
