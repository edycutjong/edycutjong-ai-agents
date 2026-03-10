import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), "standups.json")
