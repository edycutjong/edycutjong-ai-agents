"""Configuration for Bug Report Triage Agent."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Agent configuration."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL = os.getenv("MODEL", "gemini-2.0-flash")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
