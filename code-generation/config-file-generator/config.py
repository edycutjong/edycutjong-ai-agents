import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
