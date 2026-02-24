"""Receipt Categorizer Agent — core Gemini logic."""
import json
import google.generativeai as genai
from config import Config

CATEGORIZE_PROMPT = """\
You are a receipt analysis specialist. Analyze the following receipt text and produce a JSON object with:

- vendor: the store or merchant name
- date: date of purchase (or "Unknown")
- category: expense category (e.g. "Groceries", "Dining", "Transportation", "Office Supplies", "Entertainment", "Utilities", "Healthcare", "Clothing", "Electronics", "Other")
- total: total amount as a string (e.g. "$42.50")
- currency: detected currency code (e.g. "USD", "EUR", "IDR")
- items: list of objects with "name", "quantity", "price"
- payment_method: detected payment method (or "Unknown")
- tax: tax amount as a string (or "0.00")
- summary: a one-sentence summary of the purchase

Receipt text:
{receipt_text}

Respond ONLY with valid JSON.
"""


class ReceiptCategorizerAgent:
    """Categorize receipts using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def categorize(self, receipt_text: str) -> dict:
        """Analyze receipt text and return structured categorization."""
        prompt = CATEGORIZE_PROMPT.format(receipt_text=receipt_text)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
