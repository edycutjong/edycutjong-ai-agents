import pytest
from unittest.mock import MagicMock, patch



@patch("src.agent.genai")
def test_categorize_returns_dict(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"vendor": "Walmart", "date": "2024-03-15", "category": "Groceries", "total": "$42.50", "currency": "USD", "items": [{"name": "Milk", "quantity": 2, "price": "$3.99"}, {"name": "Bread", "quantity": 1, "price": "$2.49"}], "payment_method": "Visa", "tax": "$3.12", "summary": "Grocery shopping at Walmart."}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import ReceiptCategorizerAgent
    agent = ReceiptCategorizerAgent()
    result = agent.categorize("Walmart\nMilk x2  $3.99\nBread    $2.49\nTax      $3.12\nTotal    $42.50")

    assert isinstance(result, dict)
    assert result["vendor"] == "Walmart"
    assert result["category"] == "Groceries"
    assert len(result["items"]) == 2
    assert result["items"][0]["name"] == "Milk"
    mock_model.generate_content.assert_called_once()


@patch("src.agent.genai")
def test_categorize_strips_fences(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '```json\n{"vendor": "Starbucks", "date": "2024-01-10", "category": "Dining", "total": "$5.75", "currency": "USD", "items": [{"name": "Latte", "quantity": 1, "price": "$5.75"}], "payment_method": "Apple Pay", "tax": "$0.00", "summary": "Coffee purchase at Starbucks."}\n```'
    mock_model.generate_content.return_value = mock_response

    from src.agent import ReceiptCategorizerAgent
    agent = ReceiptCategorizerAgent()
    result = agent.categorize("Starbucks\nLatte $5.75")

    assert result["vendor"] == "Starbucks"
    assert result["category"] == "Dining"
    assert "Starbucks" in result["summary"]


@patch("src.agent.genai")
def test_categorize_handles_unknown_fields(mock_genai):
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = '{"vendor": "Unknown Store", "date": "Unknown", "category": "Other", "total": "$10.00", "currency": "USD", "items": [], "payment_method": "Unknown", "tax": "0.00", "summary": "Unidentified purchase."}'
    mock_model.generate_content.return_value = mock_response

    from src.agent import ReceiptCategorizerAgent
    agent = ReceiptCategorizerAgent()
    result = agent.categorize("$10.00 total")

    assert result["vendor"] == "Unknown Store"
    assert result["date"] == "Unknown"
    assert result["items"] == []
