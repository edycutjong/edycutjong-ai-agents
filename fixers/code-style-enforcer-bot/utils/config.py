import os
import json
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG = {
    "tone": "friendly",
    "ignore": ["venv", "node_modules", ".git", "__pycache__", "build", "dist"],
    "max_line_length": 88,  # Black default
    "auto_fix": False
}

CONFIG_FILE = "style-enforcer.json"

def load_config():
    """Loads configuration from file or returns default."""
    if os.path.exists(CONFIG_FILE):
        try:  # pragma: no cover
            with open(CONFIG_FILE, "r") as f:  # pragma: no cover
                user_config = json.load(f)  # pragma: no cover
                config = DEFAULT_CONFIG.copy()  # pragma: no cover
                config.update(user_config)  # pragma: no cover
                return config  # pragma: no cover
        except Exception as e:  # pragma: no cover
            # Fallback to default if error
            print(f"Error loading config: {e}")  # pragma: no cover
            return DEFAULT_CONFIG  # pragma: no cover
    return DEFAULT_CONFIG

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")  # pragma: no cover

class Config:
    def __init__(self):
        self._config = load_config()

    @property
    def tone(self):
        return self._config.get("tone", "friendly")

    @property
    def ignore_patterns(self):
        return self._config.get("ignore", [])

    @property
    def max_line_length(self):
        return self._config.get("max_line_length", 88)

    @property
    def auto_fix(self):
        return self._config.get("auto_fix", False)

config = Config()
