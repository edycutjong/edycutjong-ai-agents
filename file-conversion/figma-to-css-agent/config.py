import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")
