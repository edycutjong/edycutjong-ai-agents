import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application."""

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Model configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))

    # Supported extensions
    SUPPORTED_EXTENSIONS = {
        '.js': 'javascript',
        '.jsx': 'react',
        '.ts': 'typescript',
        '.tsx': 'react-ts',
        '.vue': 'vue',
        '.svelte': 'svelte',
        '.html': 'angular-template', # Simplified for Angular
    }

    @classmethod
    def validate_api_key(cls):
        """Check if API key is set."""
        if not cls.OPENAI_API_KEY:
            return False
        return True
