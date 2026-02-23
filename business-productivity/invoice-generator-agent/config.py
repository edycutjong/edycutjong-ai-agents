import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    STORAGE_FILE = os.path.join(os.path.dirname(__file__), "invoices.json")
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")
    COMPANY_NAME = os.getenv("COMPANY_NAME", "Acme Corp")
