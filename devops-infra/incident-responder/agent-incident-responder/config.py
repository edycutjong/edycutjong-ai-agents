"""Configuration for Incident Responder agent."""
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
LOG_PATTERNS = {
    "error": [r"ERROR", r"FATAL", r"Exception", r"Traceback"],
    "warn": [r"WARN", r"WARNING", r"Deprecat"],
    "critical": [r"CRITICAL", r"OutOfMemory", r"OOM", r"kernel panic", r"segfault"],
}
DEFAULT_SEVERITY = os.getenv("MIN_SEVERITY", "error")
