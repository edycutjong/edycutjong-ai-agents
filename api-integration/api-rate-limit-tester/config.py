import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

class AppConfig(BaseModel):
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

    # Default test settings
    default_rps: int = 10
    default_duration: int = 10
    default_burst_size: int = 5

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

config = AppConfig()

def get_config() -> AppConfig:
    return config
