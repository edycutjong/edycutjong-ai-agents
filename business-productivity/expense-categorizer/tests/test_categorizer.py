"""Tests for Expense Categorizer."""
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.categorizer import (
    categorize_transaction, parse_bank_csv, detect_recurring,
    flag_unusual_spending, generate_expense_report, format_report_markdown,
    Transaction,
)

BANK_CSV = """Date,Description,Amount
2026-01-05,STARBUCKS COFFEE,4.50
2026-01-06,UBER TRIP,12.00
2026-01-10,AMAZON PURCHASE,89.99
2026-01-15,NETFLIX SUBSCRIPTION,15.99
2026-01-15,STARBUCKS COFFEE,4.50
2026-01-20,RENT PAYMENT,1500.00
2026-01-22,CVS PHARMACY,22.50
2026-01-25,COMCAST INTERNET,79.99
2026-01-28,STEAM GAME STORE,29.99
2026-01-30,UDEMY COURSE,12.99
"""


# --- Categorization Tests ---

def test_categorize_food():
    assert categorize_transaction("STARBUCKS COFFEE") == "Food & Dining"


def test_categorize_transport():
    assert categorize_transaction("UBER TRIP") == "Transportation"


def test_categorize_shopping():
    assert categorize_transaction("AMAZON PURCHASE") == "Shopping"


def test_categorize_subscription():
    assert categorize_transaction("NETFLIX SUBSCRIPTION") == "Subscriptions"


def test_categorize_utilities():
    assert categorize_transaction("COMCAST INTERNET") == "Utilities"


def test_categorize_health():
    assert categorize_transaction("CVS PHARMACY") == "Health & Medical"


def test_categorize_entertainment():
    assert categorize_transaction("STEAM GAME STORE") == "Entertainment"


def test_categorize_education():
    assert categorize_transaction("UDEMY COURSE") == "Education"


def test_categorize_housing():
    assert categorize_transaction("RENT PAYMENT") == "Housing"


def test_categorize_unknown():
    assert categorize_transaction("RANDOM VENDOR XYZ123") == "Uncategorized"


# --- CSV Parsing Tests ---

def test_parse_bank_csv():
    """Parse CSV into categorized transactions."""
    transactions = parse_bank_csv(BANK_CSV)
    assert len(transactions) == 10
    assert all(t.category != "" for t in transactions)


def test_parse_csv_amounts():
    """Amounts are correctly parsed."""
    transactions = parse_bank_csv(BANK_CSV)
    starbucks = [t for t in transactions if "STARBUCKS" in t.description]
    assert starbucks[0].amount == 4.50


def test_parse_csv_dollar_sign():
    """Handles $ in amount column."""
    csv = "Date,Description,Amount\n2026-01-01,Test,$42.50\n"
    transactions = parse_bank_csv(csv)
    assert transactions[0].amount == 42.50


# --- Recurring Detection Tests ---

def test_detect_recurring():
    """Detects recurring transactions."""
    transactions = parse_bank_csv(BANK_CSV)
    # STARBUCKS appears twice with same amount — should be recurring
    starbucks = [t for t in transactions if "STARBUCKS" in t.description]
    assert len(starbucks) == 2
    assert all(t.is_recurring for t in starbucks)


def test_non_recurring():
    """Non-recurring transactions not flagged."""
    transactions = parse_bank_csv(BANK_CSV)
    amazon = [t for t in transactions if "AMAZON" in t.description]
    assert not amazon[0].is_recurring


# --- Report Tests ---

def test_generate_report():
    """Report has all expected fields."""
    transactions = parse_bank_csv(BANK_CSV)
    report = generate_expense_report(transactions)
    assert report["total_spending"] > 0
    assert report["transaction_count"] == 10
    assert "categories" in report
    assert len(report["categories"]) >= 5


def test_report_category_percentages():
    """Category percentages sum to ~100%."""
    transactions = parse_bank_csv(BANK_CSV)
    report = generate_expense_report(transactions)
    total_pct = sum(c["percentage"] for c in report["categories"].values())
    assert 99 <= total_pct <= 101


def test_format_markdown():
    """Markdown report contains expected sections."""
    transactions = parse_bank_csv(BANK_CSV)
    report = generate_expense_report(transactions)
    md = format_report_markdown(report, transactions)
    assert "# Expense Report" in md
    assert "## By Category" in md
    assert "Food & Dining" in md


# --- Transaction Tests ---

def test_transaction_roundtrip():
    """Transaction serializes/deserializes."""
    t = Transaction(date="2026-01-01", description="Test", amount=42.0, category="Shopping")
    d = t.to_dict()
    restored = Transaction.from_dict(d)
    assert restored.amount == 42.0
    assert restored.category == "Shopping"
