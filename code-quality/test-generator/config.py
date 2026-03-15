"""Configuration for Test Generator agent."""
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50000"))
DEFAULT_FRAMEWORK = os.getenv("DEFAULT_FRAMEWORK", "pytest")
