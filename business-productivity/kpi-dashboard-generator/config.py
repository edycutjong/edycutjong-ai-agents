import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PAGE_TITLE = "KPI Dashboard Generator"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
